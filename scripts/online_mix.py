"""Auditable toy feedback sampler, NOT a faithful implementation of DoReMi.

Scores are externally defined, standardized signals. This helper only
demonstrates temperature-softmax plus an explicit exploration floor.
"""
import math
from collections.abc import Mapping

def feedback_mixture(scores: Mapping[str, float], *, temperature: float = 1.0,
                     exploration: float = 0.10) -> dict[str, float]:
    if not scores:
        raise ValueError("scores cannot be empty")
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be finite and > 0")
    if not math.isfinite(exploration) or not 0 <= exploration <= 1:
        raise ValueError("exploration must be in [0,1]")
    names = sorted(scores)
    values = [float(scores[name]) for name in names]
    if any(not math.isfinite(value) for value in values):
        raise ValueError("all scores must be finite")
    scaled = [value / temperature for value in values]
    shift = max(scaled)
    exponentials = [math.exp(value - shift) for value in scaled]
    z = sum(exponentials)
    k = len(names)
    return {name: (1 - exploration) * value / z + exploration / k
            for name, value in zip(names, exponentials)}

def expected_token_exposure(total_tokens: int, weights: Mapping[str, float]) -> dict[str, float]:
    if isinstance(total_tokens, bool) or not isinstance(total_tokens, int) or total_tokens < 0:
        raise ValueError("total_tokens must be a non-negative integer")
    if not weights or any(not math.isfinite(float(v)) or float(v) < 0 for v in weights.values()):
        raise ValueError("weights must be non-negative finite numbers")
    if not math.isclose(sum(weights.values()), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("weights must sum to 1")
    return {key: total_tokens * float(value) for key, value in weights.items()}
