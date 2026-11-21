"""Small-sample planning helpers for binary corpus audits."""
from __future__ import annotations

import math


def required_sample_size(margin: float, z: float = 1.96, p: float = 0.5) -> int:
    """Normal-approximation sample size for a proportion, before design effects."""
    e, z_value, proportion = float(margin), float(z), float(p)
    if not math.isfinite(e) or not 0 < e < 1:
        raise ValueError("margin must be between 0 and 1")
    if not math.isfinite(z_value) or z_value <= 0:
        raise ValueError("z must be positive and finite")
    if not math.isfinite(proportion) or not 0 <= proportion <= 1:
        raise ValueError("p must be between 0 and 1")
    return math.ceil((z_value * z_value * proportion * (1 - proportion)) / (e * e))


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0:
        raise ValueError("trials must be a positive integer")
    if isinstance(successes, bool) or not isinstance(successes, int) or not 0 <= successes <= trials:
        raise ValueError("successes must be an integer in [0, trials]")
    z_value = float(z)
    if not math.isfinite(z_value) or z_value <= 0:
        raise ValueError("z must be positive and finite")
    p_hat = successes / trials
    z2 = z_value * z_value
    denominator = 1 + z2 / trials
    center = (p_hat + z2 / (2 * trials)) / denominator
    half = z_value * math.sqrt(
        p_hat * (1 - p_hat) / trials + z2 / (4 * trials * trials)
    ) / denominator
    lower = max(0.0, center - half)
    upper = min(1.0, center + half)
    # Preserve the exact mathematical endpoints despite floating-point rounding.
    if successes == 0:
        lower = 0.0
    if successes == trials:
        upper = 1.0
    return lower, upper
