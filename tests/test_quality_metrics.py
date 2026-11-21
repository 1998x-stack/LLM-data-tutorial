import unittest

from scripts.quality_metrics import required_sample_size, wilson_interval


class QualityMetricsTests(unittest.TestCase):
    def test_conservative_sample_size_for_three_percent_margin(self):
        self.assertEqual(required_sample_size(0.03), 1068)

    def test_sample_size_shrinks_with_wider_margin(self):
        self.assertGreater(required_sample_size(0.02), required_sample_size(0.05))

    def test_wilson_interval_contains_observed_rate(self):
        low, high = wilson_interval(60, 100)
        self.assertLess(low, 0.6)
        self.assertGreater(high, 0.6)

    def test_wilson_interval_handles_zero_and_all_success(self):
        low, high = wilson_interval(0, 100)
        self.assertEqual(low, 0.0)
        self.assertGreater(high, 0.0)
        low, high = wilson_interval(100, 100)
        self.assertLess(low, 1.0)
        self.assertEqual(high, 1.0)

    def test_rejects_invalid_counts_and_margins(self):
        with self.assertRaises(ValueError):
            wilson_interval(101, 100)
        with self.assertRaises(ValueError):
            wilson_interval(1, 0)
        with self.assertRaises(ValueError):
            required_sample_size(0)


if __name__ == "__main__":
    unittest.main()
