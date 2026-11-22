import unittest

from scripts.cleaning_metrics import precision_recall_f1


class CleaningMetricsTests(unittest.TestCase):
    def test_metrics_from_confusion_counts(self):
        result = precision_recall_f1(tp=800, fp=100, fn=200)
        self.assertAlmostEqual(result["precision"], 800 / 900)
        self.assertAlmostEqual(result["recall"], 0.8)
        self.assertAlmostEqual(result["f1"], 0.8421052631578948)

    def test_zero_denominators(self):
        self.assertEqual(precision_recall_f1(0, 0, 0), {
            "precision": 0.0, "recall": 0.0, "f1": 0.0
        })

    def test_negative_counts_rejected(self):
        with self.assertRaises(ValueError):
            precision_recall_f1(-1, 0, 0)


if __name__ == "__main__":
    unittest.main()
