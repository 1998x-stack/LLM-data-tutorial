import unittest

from scripts.storage_math import compressed_size_bytes, estimated_file_count, plan_storage


class StorageMathTests(unittest.TestCase):
    def test_compressed_size_uses_ceiling(self):
        self.assertEqual(compressed_size_bytes(101, 0.5), 51)

    def test_file_count_uses_ceiling(self):
        self.assertEqual(estimated_file_count(1001, 1000), 2)
        self.assertEqual(estimated_file_count(0, 1000), 0)

    def test_plan_storage(self):
        self.assertEqual(
            plan_storage(1000, 0.25, 100),
            {"raw_bytes": 1000, "compressed_bytes": 250, "estimated_file_count": 3, "target_file_bytes": 100},
        )

    def test_rejects_invalid_inputs(self):
        for args in [(-1, 0.5), (100, -0.1), (100, 1.1), (100, float("nan"))]:
            with self.assertRaises(ValueError):
                compressed_size_bytes(*args)
        with self.assertRaises(ValueError):
            estimated_file_count(10, 0)


if __name__ == "__main__":
    unittest.main()
