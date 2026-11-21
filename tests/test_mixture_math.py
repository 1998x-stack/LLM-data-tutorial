import unittest

from scripts.mixture_math import (
    document_sampling_for_token_shares,
    estimated_partition_count,
    normalize_weights,
    token_shares_from_document_sampling,
)


class MixtureMathTests(unittest.TestCase):
    def test_document_mix_is_not_token_mix(self):
        actual = token_shares_from_document_sampling([0.5, 0.5], [100, 1000])
        self.assertAlmostEqual(actual[0], 1 / 11)
        self.assertAlmostEqual(actual[1], 10 / 11)

    def test_inverse_recovers_target_token_mix(self):
        probabilities = document_sampling_for_token_shares([0.5, 0.5], [100, 1000])
        self.assertAlmostEqual(probabilities[0], 10 / 11)
        self.assertAlmostEqual(probabilities[1], 1 / 11)
        actual = token_shares_from_document_sampling(probabilities, [100, 1000])
        self.assertAlmostEqual(actual[0], 0.5)
        self.assertAlmostEqual(actual[1], 0.5)

    def test_normalize_weights(self):
        self.assertEqual(normalize_weights([2, 3, 5]), [0.2, 0.3, 0.5])

    def test_rejects_invalid_weights_and_lengths(self):
        with self.assertRaises(ValueError):
            normalize_weights([0, 0])
        with self.assertRaises(ValueError):
            token_shares_from_document_sampling([0.5, 0.5], [100])
        with self.assertRaises(ValueError):
            document_sampling_for_token_shares([0.5, 0.5], [100, 0])

    def test_partition_count_uses_ceiling(self):
        self.assertEqual(estimated_partition_count(1000, 300), 4)
        self.assertEqual(estimated_partition_count(0, 300), 0)
        with self.assertRaises(ValueError):
            estimated_partition_count(100, 0)


if __name__ == "__main__":
    unittest.main()
