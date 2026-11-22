import unittest

from scripts.domain_mix import token_exposure


class DomainMixTests(unittest.TestCase):
    def test_token_budget_split(self):
        plan = token_exposure(100_000_000_000, 0.30)
        self.assertEqual(plan["domain_tokens"], 30_000_000_000)
        self.assertEqual(plan["general_tokens"], 70_000_000_000)

    def test_zero_and_full_domain(self):
        self.assertEqual(token_exposure(10, 0)["general_tokens"], 10)
        self.assertEqual(token_exposure(10, 1)["domain_tokens"], 10)

    def test_invalid_share_rejected(self):
        with self.assertRaises(ValueError):
            token_exposure(10, 1.01)


if __name__ == "__main__":
    unittest.main()
