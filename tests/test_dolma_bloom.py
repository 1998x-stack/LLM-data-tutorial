import unittest

from scripts.dolma_bloom import bloom_filter_size


class DolmaBloomTests(unittest.TestCase):
    def test_documented_scale_example(self):
        result = bloom_filter_size(6_000_000, 0.0001)
        self.assertGreater(result["bits"], 100_000_000)
        self.assertLess(result["bits"], 120_000_000)
        self.assertGreaterEqual(result["hash_functions"], 1)
        self.assertLessEqual(result["hash_functions"], 20)

    def test_stricter_false_positive_rate_needs_more_bits(self):
        loose = bloom_filter_size(100_000, 0.01)
        strict = bloom_filter_size(100_000, 0.001)
        self.assertGreater(strict["bits"], loose["bits"])

    def test_invalid_rate_rejected(self):
        with self.assertRaises(ValueError):
            bloom_filter_size(100, 1.0)


if __name__ == "__main__":
    unittest.main()
