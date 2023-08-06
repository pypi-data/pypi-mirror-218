import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from timor.task import Solution, Task
import unittest
import requests

import cobra.solution


class TestSolutionAPI(unittest.TestCase):
    """Test solution API."""
    def test_solution_retrieval(self):
        with self.assertRaises(KeyError):
            cobra.solution.find_solutions(task_id='simple/PTP_1', version="some-not-existing-version")
        solutions = cobra.solution.find_solutions(task_id='simple/PTP_1')
        self.assertGreater(len(solutions), 0)
        for solution in solutions:
            self.assertIsNotNone(solution['id'])
            self.assertIsNotNone(solution['costFunction'])
            self.assertIsNotNone(solution['cost'])
            self.assertEqual(requests.get(solution['json']).status_code, 200)

    def test_solution_file_retrieval(self):
        solutions = cobra.solution.find_solutions(task_id='simple/PTP_1')
        solution_file, task_file = cobra.solution.get_solution(solutions[0]['id'])
        self.assertTrue(solution_file.is_file())
        self.assertTrue(task_file.is_file())
        self.assertIsNotNone(json.load(solution_file.open()))
        self.assertIsNotNone(json.load(task_file.open()))
        timor_task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(timor_task)
        timor_solution = Solution.SolutionTrajectory.from_json_file(solution_file, {timor_task.id: timor_task})
        self.assertIsNotNone(timor_solution)
        self.assertIsNotNone(timor_solution.cost)

    def test_solution_upload(self):  # TODO Alters test data base -> should be run in a separate test environment
        solutions = cobra.solution.find_solutions(task_id='simple/PTP_1')
        solution_file, task_file = cobra.solution.get_solution(solutions[0]['id'])
        solution_data = json.load(solution_file.open())
        solution_data['author'].append('CoBRA I/O Test Case')
        with tempfile.NamedTemporaryFile("w") as tmp_file:
            json.dump(solution_data, tmp_file)
            tmp_file.flush()
            with patch('builtins.input', return_value='!2345678'):
                cobra.solution.submit_solution(Path(tmp_file.name), "m@tum.de")  # TODO add test user
