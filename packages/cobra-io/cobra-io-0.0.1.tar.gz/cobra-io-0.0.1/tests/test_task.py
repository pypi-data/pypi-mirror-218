import json
from timor.task import Task
import unittest
import requests

import cobra.task
from cobra.utils import caches
from cobra.utils.configurations import COBRA_VERSION


class TestTaskAPI(unittest.TestCase):
    """Test task API."""
    def test_task_retrieval(self):
        caches.reset_cache()
        task_file = cobra.task.get_task(id='simple/PTP_1')
        self.assertTrue(task_file.is_file())
        self.assertIsNotNone(json.load(task_file.open()))
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
        with self.assertRaises(ValueError):
            cobra.task.get_task(version='some-not-existing-version')

    def test_find_tasks(self):
        caches.reset_cache()
        candidates, details = cobra.task.find_tasks(id='simple/PTP_1')
        self.assertEqual(len(candidates), 1)
        # Check details
        self.assertEqual(len(details), 1)
        self.assertEqual(details[0]['scenario_id'], 'simple/PTP_1')
        self.assertEqual(details[0]['version'], COBRA_VERSION)
        self.assertEqual(requests.get(details[0]['html']).status_code, 200)
        self.assertEqual(requests.get(details[0]['json']).status_code, 200)
        self.assertEqual(details[0]['metadata']['goal_count'], 2)
        task_file = cobra.task.get_task(uuid=details[0]['id'])
        self.assertTrue(task_file.is_file())
        self.assertIsNotNone(json.load(task_file.open()))
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
        # Check wrong version
        candidates, details = cobra.task.find_tasks(id='simple/PTP_1', version='some-not-existing-version')
        self.assertEqual(len(candidates), 0)
        # Check wrong id
        candidates, details = cobra.task.find_tasks(id='some-not-existing-id')
        self.assertEqual(len(candidates), 0)

    def test_task_with_asset(self):
        caches.reset_cache()
        task_file = cobra.task.get_task(id='simple/PTP_2', fetch_assets=False)
        with self.assertRaises(FileNotFoundError):
            Task.Task.from_json_file(task_file)
        task_file = cobra.task.get_task(id='simple/PTP_2', fetch_assets=True)
        task = Task.Task.from_json_file(task_file)
        self.assertIsNotNone(task)
