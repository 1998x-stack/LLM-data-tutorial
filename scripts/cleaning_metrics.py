"""Confusion-matrix metrics for audited binary cleaning decisions."""


def precision_recall_f1(tp: int, fp: int, fn: int) -> dict[str, float]:
    """Compute precision, recall and F1; undefined denominators return zero."""
    for name, value in (("tp", tp), ("fp", fp), ("fn", fn)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{name} must be a non-negative integer")
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
