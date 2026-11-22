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
        allowed_kinds = {"paper-result", "paper-method", "official-doc", "implementation", "derived", "illustrative", "standard"}
        allowed_statuses = {"verified", "derived", "illustrative", "unverified"}
        for number in tuple(f"{index:02d}" for index in range(1, 26)):
            path = ROOT / "evidence" / f"{number}.json"
            self.assertTrue(path.is_file())
            ledger = json.loads(path.read_text(encoding="utf-8"))
            minimum_claims = 3 if number <= "05" else 5
            self.assertGreaterEqual(len(ledger["claims"]), minimum_claims)
            claim_ids = [claim["id"] for claim in ledger["claims"]]
            self.assertEqual(len(claim_ids), len(set(claim_ids)))
            for claim in ledger["claims"]:
                for field in ("id", "claim", "kind", "source_url", "locator", "status", "notes"):
                    self.assertTrue(str(claim.get(field, "")).strip(), f"{number}: missing {field}")
                self.assertIn(claim["kind"], allowed_kinds, f"{number}: unsupported evidence kind")
                self.assertIn(claim["status"], allowed_statuses, f"{number}: unsupported evidence status")
                self.assertTrue(claim["source_url"].startswith("https://"), f"{number}: source must use HTTPS")

    def test_data_tooling_examples_are_release_pinned(self):
        chapter23 = (ROOT / "23.html").read_text(encoding="utf-8")
        self.assertIn('datatrove[io,processing]==0.10.1', chapter23)
        self.assertIn('blob/v0.10.1/', chapter23)
        self.assertNotIn('datatrove/blob/main/', chapter23)
        chapter24 = (ROOT / "24.html").read_text(encoding="utf-8")
        self.assertIn('dolma==1.2.1', chapter24)
        self.assertIn('blob/v1.2.1/', chapter24)
        self.assertIn('1a9daced81670e0fa768e47fbed32af6694a1865', chapter24)
        self.assertNotIn('*.json.gz', chapter24)

    def test_batch_five_evidence_is_source_located(self):
        for number in ("21", "22", "23", "24", "25"):
            ledger = json.loads((ROOT / "evidence" / f"{number}.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(ledger["claims"]), 8)
            for claim in ledger["claims"]:
                self.assertTrue(claim.get("source_url"), claim.get("id"))
                self.assertTrue(claim.get("locator"), claim.get("id"))
                self.assertTrue(claim.get("notes"), claim.get("id"))
                self.assertIn(claim.get("kind"), {"paper-result", "paper-method", "official-doc", "implementation", "derived", "illustrative", "standard"})


if __name__ == "__main__":
    unittest.main()
