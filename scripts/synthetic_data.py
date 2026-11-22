"""Planning helpers for sequential synthetic-data quality gates."""
from math import prod
from collections.abc import Sequence


def estimate_accepted_records(
    generated: int,
    stage_retention_rates: Sequence[float],
) -> float:
    """Return expected survivors from sequential conditional stage rates.

    Each rate must be measured on the output of the immediately previous
    stage. This is an expected-value estimate, not an observed integer count.
    """
    if isinstance(generated, bool) or not isinstance(generated, int) or generated < 0:
        raise ValueError("generated must be a non-negative integer")
    rates = tuple(float(rate) for rate in stage_retention_rates)
    if any(rate < 0.0 or rate > 1.0 for rate in rates):
        raise ValueError("each retention rate must be between 0 and 1")
    return generated * prod(rates)
