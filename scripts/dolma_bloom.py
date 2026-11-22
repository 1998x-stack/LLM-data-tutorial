"""Classical Bloom-filter bit-array sizing approximation."""
from math import ceil, log


def bloom_filter_size(expected_items: int, false_positive_rate: float) -> dict[str, int | float]:
    """Estimate bit count, byte count and optimal hash count.

    Excludes process overhead, object storage, buffers and implementation details.
    """
    if isinstance(expected_items, bool) or not isinstance(expected_items, int) or expected_items <= 0:
        raise ValueError("expected_items must be a positive integer")
    rate = float(false_positive_rate)
    if not 0.0 < rate < 1.0:
        raise ValueError("false_positive_rate must be between 0 and 1")
    ln2 = log(2.0)
    bits = ceil(-expected_items * log(rate) / (ln2 * ln2))
    hashes = max(1, round((bits / expected_items) * ln2))
    byte_count = ceil(bits / 8)
    return {
        "bits": bits,
        "bytes": byte_count,
        "mib": byte_count / (1024 * 1024),
        "hash_functions": hashes,
    }
