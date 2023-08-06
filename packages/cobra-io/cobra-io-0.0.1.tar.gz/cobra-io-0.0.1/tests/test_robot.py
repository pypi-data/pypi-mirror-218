import json
import unittest

import cobra


class TestRobotAPI(unittest.TestCase):
    """Test robot API."""
    def test_all_downloadable(self):
        robots = cobra.robot.get_available_module_dbs()
        for robot in robots:
            f = cobra.robot.get_module_db(robot)
            self.assertTrue(f.is_file())
            data = json.load(f.open())
            self.assertTrue('modules' in data)
            self.assertTrue(len(data['modules']) > 0)

        local_robots = cobra.robot.get_available_module_dbs(locally=True)
        self.assertEqual(robots, local_robots)
        for robot in robots:
            f = cobra.robot.get_module_db(robot)
            self.assertTrue(f.is_file())
            data = json.load(f.open())
            self.assertTrue('modules' in data)
            self.assertTrue(len(data['modules']) > 0)
