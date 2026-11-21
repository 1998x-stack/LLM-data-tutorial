"""Small, dependency-free utilities for reasoning about document-vs-token mixtures.

The conversion assumes independent document sampling and stationary mean lengths.
It is a planning approximation; measure the final packed token stream in production.
"""
from __future__ import annotations

import math
from collections.abc import Sequence


def _validate(values: Sequence[float], name: str, *, positive: bool = False) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError(f"{name} must not be empty")
    for value in result:
        if not math.isfinite(value):
            raise ValueError(f"{name} must contain finite values")
        if value < 0 or (positive and value <= 0):
            raise ValueError(f"{name} contains an invalid value")
    return result


def normalize_weights(weights: Sequence[float]) -> list[float]:
    """Normalize non-negative weights to sum to one."""
    values = _validate(weights, "weights")
    total = sum(values)
    if total <= 0:
        raise ValueError("weights must have a positive sum")
    return [value / total for value in values]


def token_shares_from_document_sampling(
    document_probabilities: Sequence[float],
    mean_tokens: Sequence[float],
) -> list[float]:
    """Expected token shares q_i ∝ p_i * mean_tokens_i."""
    p = normalize_weights(document_probabilities)
    means = _validate(mean_tokens, "mean_tokens", positive=True)
    if len(p) != len(means):
        raise ValueError("document_probabilities and mean_tokens must have equal length")
    return normalize_weights([probability * mean for probability, mean in zip(p, means)])


def document_sampling_for_token_shares(
    target_token_shares: Sequence[float],
    mean_tokens: Sequence[float],
) -> list[float]:
    """Invert the approximation: p_i ∝ q_i / mean_tokens_i."""
    q = normalize_weights(target_token_shares)
    means = _validate(mean_tokens, "mean_tokens", positive=True)
    if len(q) != len(means):
        raise ValueError("target_token_shares and mean_tokens must have equal length")
    return normalize_weights([share / mean for share, mean in zip(q, means)])


def estimated_partition_count(total_bytes: int, target_partition_bytes: int) -> int:
    """Ceiling division for a planning estimate; ignores file splittability and skew."""
    if total_bytes < 0 or target_partition_bytes <= 0:
        raise ValueError("total_bytes must be non-negative and target_partition_bytes positive")
    return (total_bytes + target_partition_bytes - 1) // target_partition_bytes
