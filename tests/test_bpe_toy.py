import unittest

from scripts.bpe_toy import encode_word, train_bpe


class BpeToyTests(unittest.TestCase):
    def test_training_is_deterministic(self):
        corpus = ["low", "lower", "lowest", "low", "lowest"]
        self.assertEqual(train_bpe(corpus, 8), train_bpe(corpus, 8))

    def test_more_merges_do_not_increase_token_count_for_same_word(self):
        corpus = ["low", "lower", "lowest", "low", "lowest"]
        few = encode_word("lowest", train_bpe(corpus, 2))
        many = encode_word("lowest", train_bpe(corpus, 8))
        self.assertLessEqual(len(many), len(few))

    def test_zero_merges_preserves_character_units_and_end_marker(self):
        self.assertEqual(encode_word("cat", []), ("c", "a", "t", "</w>"))

    def test_merges_can_form_whole_word(self):
        merges = train_bpe(["low", "low", "low"], 4)
        encoded = encode_word("low", merges)
        self.assertEqual(len(encoded), 1)

    def test_rejects_invalid_training_inputs(self):
        with self.assertRaises(ValueError):
            train_bpe(["low"], -1)
        with self.assertRaises(ValueError):
            train_bpe([""], 2)
        with self.assertRaises(ValueError):
            encode_word("", [])


if __name__ == "__main__":
    unittest.main()
