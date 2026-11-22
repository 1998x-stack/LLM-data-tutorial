import unittest
from scripts.review_repo import review

class FullRepositoryReviewTests(unittest.TestCase):
    def test_all_28_chapters_audited(self):
        result = review()
        self.assertEqual(result["chapters"], 28)
        self.assertEqual(len(result["pages"]), 28)
        self.assertEqual(result["errors"], [], "\n".join(result["errors"]))

    def test_evidence_and_diagrams_coverage(self):
        result = review()
        self.assertGreaterEqual(result["diagrams"], 50)
        self.assertGreaterEqual(result["referenced_diagrams"], 40)
        for number in range(1, 29):
            page = result["pages"][f"{number:02d}"]
            self.assertTrue(page["evidence"])
            self.assertGreaterEqual(page["figures"], 1)

if __name__ == "__main__": unittest.main()
