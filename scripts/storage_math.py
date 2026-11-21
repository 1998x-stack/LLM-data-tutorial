"""Capacity-planning arithmetic for large corpus storage.

This module does not predict compression performance. The compression ratio is
an explicit measured or assumed input supplied by the caller.
"""
from __future__ import annotations

import math


def compressed_size_bytes(raw_bytes: int, compressed_fraction: float) -> int:
    """Return ceil(raw_bytes * compressed_fraction)."""
    if isinstance(raw_bytes, bool) or not isinstance(raw_bytes, int) or raw_bytes < 0:
        raise ValueError("raw_bytes must be a non-negative integer")
    ratio = float(compressed_fraction)
    if not math.isfinite(ratio) or not 0 <= ratio <= 1:
        raise ValueError("compressed_fraction must be finite and between 0 and 1")
    return math.ceil(raw_bytes * ratio)


def estimated_file_count(compressed_bytes: int, target_file_bytes: int) -> int:
    """Estimate file count using ceiling division; ignores metadata and skew."""
    if isinstance(compressed_bytes, bool) or not isinstance(compressed_bytes, int) or compressed_bytes < 0:
        raise ValueError("compressed_bytes must be a non-negative integer")
    if isinstance(target_file_bytes, bool) or not isinstance(target_file_bytes, int) or target_file_bytes <= 0:
        raise ValueError("target_file_bytes must be a positive integer")
    return (compressed_bytes + target_file_bytes - 1) // target_file_bytes


def plan_storage(raw_bytes: int, compressed_fraction: float, target_file_bytes: int) -> dict:
    compressed = compressed_size_bytes(raw_bytes, compressed_fraction)
    return {
        "raw_bytes": raw_bytes,
        "compressed_bytes": compressed,
        "estimated_file_count": estimated_file_count(compressed, target_file_bytes),
        "target_file_bytes": target_file_bytes,
    }
