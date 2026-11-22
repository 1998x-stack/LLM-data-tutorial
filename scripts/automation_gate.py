"""Deterministic review gate for a candidate data batch.

A READY decision is permission to request publication approval, never
permission for an agent to deploy or to bypass legal/privacy review.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class GateDecision:
    status: str
    reasons: tuple[str, ...]
    retention: float

def evaluate_batch(*, input_docs: int, accepted_docs: int, hard_violations: int,
                   audited_docs: int, min_retention: float = 0.50,
                   min_audit_fraction: float = 0.10) -> GateDecision:
    for label, value in (("input_docs", input_docs), ("accepted_docs", accepted_docs),
                         ("hard_violations", hard_violations), ("audited_docs", audited_docs)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{label} must be a non-negative integer")
    if input_docs == 0 or accepted_docs > input_docs or audited_docs > input_docs:
        raise ValueError("input_docs must be positive, and counts must not exceed input_docs")
    if not 0 <= min_retention <= 1 or not 0 <= min_audit_fraction <= 1:
        raise ValueError("thresholds must be within [0, 1]")
    retention = accepted_docs / input_docs
    reasons = []
    if hard_violations:
        reasons.append("hard_governance_violation")
    if retention < min_retention:
        reasons.append("retention_below_threshold")
    if audited_docs / input_docs < min_audit_fraction:
        reasons.append("audit_coverage_below_threshold")
    if hard_violations:
        status = "BLOCK"
    elif reasons:
        status = "REVIEW"
    else:
        status = "READY_FOR_HUMAN_APPROVAL"
    return GateDecision(status, tuple(reasons), retention)
