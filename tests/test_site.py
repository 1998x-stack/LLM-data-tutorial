import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))

    def test_chapter_numbers_and_files_are_sequential(self):
        self.assertEqual(len(self.catalog["chapters"]), 28)
        for index, chapter in enumerate(self.catalog["chapters"], 1):
            number = f"{index:02d}"
            self.assertEqual(chapter["num"], number)
            self.assertEqual(chapter["file"], number + ".html")
            self.assertTrue((ROOT / chapter["file"]).is_file())

    def test_categories_are_unique_and_referenced(self):
        ids = [category["id"] for category in self.catalog["categories"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(chapter["category"] in ids for chapter in self.catalog["chapters"]))

    def test_every_chapter_has_summary_tags_and_level(self):
        for chapter in self.catalog["chapters"]:
            self.assertTrue(chapter["summary"].strip())
            self.assertTrue(chapter["tags"])
            self.assertTrue(chapter["level"])

    def test_first_twenty_five_chapters_have_evidence_ledgers(self):
        allowed_kinds = {"paper-result", "paper-method", "official-doc", "implementation", "derived", "illustrative"}
        allowed_statuses = {"verified", "derived", "illustrative", "unverified"}
        for number in tuple(f"{index:02d}" for index in range(1, 26)):
            path = ROOT / "evidence" / f"{number}.json"
            self.assertTrue(path.is_file())
            ledger = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(ledger["chapter"], number)
            minimum_claims = 3 if number <= "05" else 5
            self.assertGreaterEqual(len(ledger["claims"]), minimum_claims)
            claim_ids = [claim["id"] for claim in ledger["claims"]]
            self.assertEqual(len(claim_ids), len(set(claim_ids)))
            for claim in ledger["claims"]:
                for field in ("id", "claim", "kind", "source_url", "locator", "status", "notes"):
                    self.assertTrue(str(claim.get(field, "")).strip(), f"{number}: missing {field}")
                self.assertIn(claim["kind"], allowed_kinds, f"{number}: unsupported kind")
                self.assertIn(claim["status"], allowed_statuses, f"{number}: unsupported status")
                self.assertTrue(claim["source_url"].startswith("https://"), f"{number}: source must use HTTPS")


if __name__ == "__main__":
    unittest.main()
