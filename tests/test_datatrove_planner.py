import unittest

from scripts.datatrove_planner import plan_tasks


class DataTrovePlannerTests(unittest.TestCase):
    def test_tasks_and_workers_are_distinct(self):
        plan = plan_tasks(file_count=10_000, tasks=1_000, workers=100)
        self.assertEqual(plan["active_tasks_upper_bound"], 1_000)
        self.assertEqual(plan["concurrent_tasks_upper_bound"], 100)
        self.assertEqual(plan["estimated_files_per_task_ceiling"], 10)

    def test_more_tasks_than_files_leaves_empty_tasks(self):
        plan = plan_tasks(file_count=10, tasks=20, workers=8)
        self.assertEqual(plan["active_tasks_upper_bound"], 10)
        self.assertEqual(plan["empty_tasks_lower_bound"], 10)
        self.assertEqual(plan["concurrent_tasks_upper_bound"], 8)

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            plan_tasks(0, 1, 1)


if __name__ == "__main__":
    unittest.main()
