import argparse
import json
from pathlib import Path
from typing import Optional, Tuple

import requests

from cobra.user.user import login
from cobra.utils.caches import SOLUTION_CACHE
from cobra.utils.configurations import COBRA_VERSION
import cobra.utils.logging as logging
from cobra.task.task import find_tasks, get_task
from cobra.utils.urls import RANKING_URL, SOLUTION_URL


def find_solutions(task_id: Optional[str] = None, task_uuid: Optional[str] = None, version: str = COBRA_VERSION,
                   cost_function: Optional[str] = None):
    """
    Return a list of solutions for the given task.

    :param task_id: The id of the task the solutions belong to.
    :param task_uuid: The uuid of the task the solutions belong to.
    :param version: The version of the CoBRA benchmark to use.
    :return: A list of solutions.
    """
    if task_uuid is None and task_id is None:
        raise ValueError("Either task_uuid or task_id must be given.")
    if task_uuid is None:
        _, details = find_tasks(id=task_id, version=version)
        if len(details) != 1:
            raise KeyError(f"Task with id {task_id} not unique in version {version}.")
        task_uuid = details[0]['id']
    query = RANKING_URL + task_uuid + "/"
    if cost_function is not None:
        query += f"?costFunction__icontains={cost_function}"
    r = requests.get(query)
    if r.status_code != 200:
        raise ValueError(f"Solutions for task with uuid {task_uuid} not found.")
    if r.json()['next'] is not None:
        logging.warning(f"Only the first {r.json()['count']} solutions are returned.")
    return r.json()['results']


def get_solution(solution_uuid: str, force_download: bool = False) -> Tuple[Path, Path]:
    """
    Return a solution file with the given uuid.

    :param solution_uuid: The uuid of the solution to return.
    :param force_download: Whether to force download the solution file.
    :return: The solution file and associated task file.
    """
    solution_file = SOLUTION_CACHE.joinpath(solution_uuid + ".json")
    if solution_file.exists() and not force_download:
        logging.debug("Solution file already exists. Returning cached version.")
        solution_data = json.load(solution_file.open("r"))
        return solution_file, get_task(id=solution_data["taskID"], version=solution_data["version"])

    r = requests.get(SOLUTION_URL + solution_uuid + "/")
    if r.status_code != 200:
        raise ValueError(f"Solution with uuid {solution_uuid} not available.")
    r_json = requests.get(r.json()["json"])
    if r_json.status_code != 200:
        raise ValueError(f"Solution json for uuid {solution_uuid} not available.")

    with open(solution_file, "wb") as f:
        f.write(r_json.content)

    task_file = get_task(uuid=r.json()["scenario_id"], force_download=force_download)

    return solution_file, task_file


def submit_solution(solution_file: Path, user_email: str):
    """
    Submit a solution file to the CoBRA benchmark.

    :param solution_file: The solution file to submit.
    :param user_email: The email of the user submitting the solution.
    :note: Might need CLI input for password.
    """
    access_token = login(user_email)
    r = requests.post(SOLUTION_URL + 'solutionsupload/upload/',
                      files={"json": solution_file.open("rb")},
                      headers={"Authorization": f"Bearer {access_token}"})
    if r.status_code != 201:
        if r.status_code == 400 and b'Set overwrite=True in order to overwrite' in r.content:
            logging.info("Solution already exists. Did not overwrite.")
            return True
        raise ValueError(f"Solution upload failed with status code {r.status_code}; details: {r.content}.")
    return True


def main():
    """Entry point to use solution as a command line tool for solution overview and file retrieval."""
    parser = argparse.ArgumentParser(description="Download solutions from the CoBRA benchmark.")
    parser.add_argument("--task_id", type=str, help="The id of the task to download solutions for.", default=None)
    parser.add_argument("--task_uuid", type=str, help="The uuid of the task to download solutions for.", default=None)
    parser.add_argument("--solution_uuid", type=str, help="The uuid of the solution to download.", default=None)
    parser.add_argument("--version", type=str, default=COBRA_VERSION, help="The version of the CoBRA benchmark to use.")
    parser.add_argument("--cost_function", type=str, default=None,
                        help="The cost function to use when querying solutions to a task.")
    args = parser.parse_args()

    if args.task_id is None and args.task_uuid is None and args.solution_uuid is None:
        raise ValueError("Either task_id, task_uuid, or solution_uuid must be given.")

    if args.solution_uuid is not None:
        if args.task_id is not None or args.task_uuid is not None:
            logging.warning("Ignoring task_id and task_uuid as solution_uuid is given.")
        solution, task = get_solution(args.solution_uuid)
        print(f"Solution file: {solution}, Task file: {task}")
    else:
        solutions = find_solutions(task_id=args.task_id, task_uuid=args.task_uuid, version=args.version,
                                   cost_function=args.cost_function)
        print(f"Found {len(solutions)} solutions for task {args.task_id} in version {args.version}.")
        print("Solution id                          | Cost     | Cost function")
        print("-------------------------------------+----------+--------------")
        for solution in solutions:
            print(f"{solution['id']} | {solution['cost']:8.2f} | {solution['costFunction']}")
    return 0


if __name__ == "__main__":
    main()
