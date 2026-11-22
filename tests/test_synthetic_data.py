import unittest

from scripts.synthetic_data import estimate_accepted_records


class SyntheticDataTests(unittest.TestCase):
    def test_sequential_conditional_retention(self):
        self.assertAlmostEqual(
            estimate_accepted_records(10_000, [0.95, 0.75, 0.85, 0.98]),
            5_935.125,
        )

    def test_empty_stages_keep_all(self):
        self.assertEqual(estimate_accepted_records(12, []), 12)

    def test_zero_generated(self):
        self.assertEqual(estimate_accepted_records(0, [0.5]), 0)

    def test_invalid_rate_rejected(self):
        with self.assertRaises(ValueError):
            estimate_accepted_records(10, [1.1])


if __name__ == "__main__":
    unittest.main()
