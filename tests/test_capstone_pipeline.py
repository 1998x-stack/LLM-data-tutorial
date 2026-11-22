import json
import tempfile
import unittest
from pathlib import Path
from scripts.capstone_pipeline import build_release, verify_release

ROOT = Path(__file__).resolve().parents[1]

class CapstonePipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.input = ROOT / "examples/capstone/raw.jsonl"
        self.policy = ROOT / "examples/capstone/policy.json"
        self.out = Path(self.tmp.name)

    def test_fixtures_have_deterministic_acceptance(self):
        path, manifest = build_release(self.input, self.policy, self.out)
        self.assertEqual(manifest["accepted_docs"], 5)
        self.assertEqual(manifest["rejected_docs"], 7)
        self.assertEqual(manifest["gate"], "READY_FOR_HUMAN_APPROVAL")
        self.assertEqual(verify_release(path), manifest)
        report = json.loads((path / "quality_report.json").read_text())
        self.assertEqual(report["rejection_reasons"]["duplicate_text"], 1)
        self.assertEqual(report["rejection_reasons"]["evaluation_holdout_id"], 1)

    def test_second_run_is_idempotent(self):
        path_a, manifest_a = build_release(self.input, self.policy, self.out)
        path_b, manifest_b = build_release(self.input, self.policy, self.out)
        self.assertEqual(path_a, path_b)
        self.assertEqual(manifest_a, manifest_b)
        self.assertEqual(len(list(self.out.iterdir())), 1)

    def test_modified_input_creates_distinct_release(self):
        copied = self.out / "updated.jsonl"
        copied.write_bytes(self.input.read_bytes() + b'not-json\n')
        first, _ = build_release(self.input, self.policy, self.out)
        second, manifest = build_release(copied, self.policy, self.out)
        self.assertNotEqual(first, second)
        self.assertEqual(manifest["input_docs"], 13)
        self.assertEqual(manifest["rejected_docs"], 8)

    def test_tampered_output_rejected(self):
        path, _ = build_release(self.input, self.policy, self.out)
        with (path / "curated.jsonl").open("ab") as handle:
            handle.write(b'bad\n')
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            verify_release(path)

    def test_policy_change_affects_run_id_and_gate(self):
        obj = json.loads(self.policy.read_text())
        obj["min_accepted"] = 99
        alternate = self.out / "alternate-policy.json"
        alternate.write_text(json.dumps(obj), encoding="utf-8")
        path, manifest = build_release(self.input, alternate, self.out)
        self.assertEqual(manifest["gate"], "HOLD_FOR_REVIEW")
        self.assertEqual(verify_release(path), manifest)

    def test_invalid_policy_fails_closed(self):
        obj = json.loads(self.policy.read_text())
        del obj["allowed_sources"]
        bad = self.out / "bad-policy.json"
        bad.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "allowed_sources"):
            build_release(self.input, bad, self.out)

    def test_rejected_data_never_contains_raw_text(self):
        path, _ = build_release(self.input, self.policy, self.out)
        rejected = (path / "rejected.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("这是未经许可", rejected)
        self.assertNotIn('"text"', rejected)

if __name__ == "__main__": unittest.main()
