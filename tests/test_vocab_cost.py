import unittest

from scripts.vocab_cost import logits_elements, vocabulary_parameter_count, vocabulary_weight_bytes


class VocabularyCostTests(unittest.TestCase):
    def test_tied_and_untied_parameter_counts(self):
        self.assertEqual(vocabulary_parameter_count(1000, 100, True), 100_000)
        self.assertEqual(vocabulary_parameter_count(1000, 100, False), 200_000)

    def test_bf16_weight_bytes(self):
        self.assertEqual(vocabulary_weight_bytes(1000, 100, 2, True), 200_000)

    def test_logits_shape(self):
        self.assertEqual(logits_elements(2, 128, 1000), 256_000)

    def test_rejects_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            vocabulary_parameter_count(0, 100, True)
        with self.assertRaises(ValueError):
            logits_elements(1, 0, 1000)


if __name__ == "__main__":
    unittest.main()
