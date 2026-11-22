import unittest
from scripts.automation_gate import evaluate_batch

class AutomationGateTests(unittest.TestCase):
    def test_ready_requires_all_checks(self):
        result = evaluate_batch(input_docs=1000, accepted_docs=800, hard_violations=0, audited_docs=120)
        self.assertEqual(result.status, "READY_FOR_HUMAN_APPROVAL")
        self.assertEqual(result.retention, 0.8)
    def test_governance_hard_blocks_regardless_of_quality(self):
        result = evaluate_batch(input_docs=1000, accepted_docs=980, hard_violations=1, audited_docs=1000)
        self.assertEqual(result.status, "BLOCK")
    def test_low_audit_coverage_requires_review(self):
        result = evaluate_batch(input_docs=100, accepted_docs=80, hard_violations=0, audited_docs=1)
        self.assertEqual(result.status, "REVIEW")
        self.assertIn("audit_coverage_below_threshold", result.reasons)
    def test_zero_input_is_invalid(self):
        with self.assertRaises(ValueError):
            evaluate_batch(input_docs=0, accepted_docs=0, hard_violations=0, audited_docs=0)
    def test_counts_cannot_exceed_input(self):
        with self.assertRaises(ValueError):
            evaluate_batch(input_docs=10, accepted_docs=11, hard_violations=0, audited_docs=0)
if __name__ == "__main__": unittest.main()
