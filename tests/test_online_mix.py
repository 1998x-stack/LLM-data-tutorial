import math
import unittest
from scripts.online_mix import feedback_mixture, expected_token_exposure

class FeedbackMixtureTests(unittest.TestCase):
    def test_equal_scores_uniform(self):
        w = feedback_mixture({"a": 1, "b": 1, "c": 1})
        self.assertAlmostEqual(w["a"], 1/3)
        self.assertAlmostEqual(sum(w.values()), 1)
    def test_exploration_provides_floor(self):
        w = feedback_mixture({"b": 0, "a": 1000}, temperature=0.1, exploration=0.2)
        self.assertGreaterEqual(w["b"], 0.1)
        self.assertAlmostEqual(sum(w.values()), 1)
    def test_temperature_changes_concentration(self):
        s = {"a": 4, "b": 1}
        low = feedback_mixture(s, temperature=0.5, exploration=0)
        high = feedback_mixture(s, temperature=3, exploration=0)
        self.assertGreater(low["a"], high["a"])
    def test_bad_values_rejected(self):
        for kw in ({"temperature":0}, {"exploration":1.2}):
            with self.assertRaises(ValueError): feedback_mixture({"a": 1}, **kw)
        with self.assertRaises(ValueError): feedback_mixture({"a":math.inf})
    def test_token_exposure_matches_weights(self):
        self.assertEqual(expected_token_exposure(1000, {"a":0.3, "b":0.7})["a"], 300)
    def test_weights_must_sum_to_one(self):
        with self.assertRaises(ValueError): expected_token_exposure(100, {"a":0.6})
if __name__ == "__main__": unittest.main()
