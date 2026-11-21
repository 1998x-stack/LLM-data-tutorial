"""Small, dependency-free primitives used in the deduplication chapters.

These are teaching/reference implementations, not a distributed production pipeline.
"""
from __future__ import annotations

import hashlib
import math
from urllib.parse import unquote_plus, urlsplit, urlunsplit


def canonicalize_url(url: str, tracking_params: set[str] | None = None) -> str:
    """Conservatively normalize a crawl URL without changing path/query semantics.

    - lowercases scheme and host;
    - removes default HTTP(S) ports and fragments;
    - removes only known tracking keys (utm_*, plus an explicit allowlist);
    - preserves path case, query value case, and query parameter order.

    Userinfo is rejected because credentials should not be embedded in crawl URLs.
    """
    parts = urlsplit(url.strip())
    if not parts.scheme or not parts.hostname:
        raise ValueError("absolute URL with scheme and host required")
    if parts.username is not None or parts.password is not None:
        raise ValueError("userinfo is not supported in crawl URLs")

    scheme = parts.scheme.lower()
    host = parts.hostname.encode("idna").decode("ascii").lower()
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    port = parts.port
    default_port = (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    netloc = host if port is None or default_port else f"{host}:{port}"

    known_tracking = {key.lower() for key in (tracking_params or set())}
    kept_query = []
    for item in parts.query.split("&") if parts.query else []:
        raw_key = item.split("=", 1)[0]
        key = unquote_plus(raw_key).lower()
        if key.startswith("utm_") or key in known_tracking:
            continue
        kept_query.append(item)

    return urlunsplit((scheme, netloc, parts.path, "&".join(kept_query), ""))


def content_digest(text: str) -> bytes:
    """SHA-256 fingerprint of the exact UTF-8 text supplied by the caller."""
    return hashlib.sha256(text.encode("utf-8")).digest()


def jaccard_similarity(left: set, right: set) -> float:
    """Jaccard similarity for two feature sets; empty/empty is defined as 1."""
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def lsh_candidate_probability(similarity: float, bands: int, rows: int) -> float:
    """Probability 1 - (1 - s**rows)**bands under independent-band assumptions."""
    if not 0.0 <= similarity <= 1.0:
        raise ValueError("similarity must be in [0, 1]")
    if bands <= 0 or rows <= 0:
        raise ValueError("bands and rows must be positive")
    return 1.0 - (1.0 - similarity**rows) ** bands


def bloom_parameters(capacity: int, false_positive_rate: float) -> tuple[int, int]:
    """Return approximate (m bits, k hashes) for a target false-positive rate."""
    if capacity <= 0:
        raise ValueError("capacity must be positive")
    if not 0.0 < false_positive_rate < 1.0:
        raise ValueError("false_positive_rate must be in (0, 1)")
    m = math.ceil(-capacity * math.log(false_positive_rate) / (math.log(2) ** 2))
    k = max(1, round((m / capacity) * math.log(2)))
    return m, k


class BloomFilter:
    """Insertion-only Bloom filter: false positives possible, false negatives absent."""

    def __init__(self, capacity: int, false_positive_rate: float = 0.01):
        self.capacity = capacity
        self.bit_count, self.hash_count = bloom_parameters(capacity, false_positive_rate)
        self.bits = bytearray((self.bit_count + 7) // 8)

    @staticmethod
    def _as_bytes(item: str | bytes) -> bytes:
        return item.encode("utf-8") if isinstance(item, str) else item

    def _positions(self, item: str | bytes):
        digest = hashlib.sha256(self._as_bytes(item)).digest()
        h1 = int.from_bytes(digest[:16], "big")
        h2 = int.from_bytes(digest[16:], "big") | 1
        while math.gcd(h2, self.bit_count) != 1:
            h2 += 2
        for index in range(self.hash_count):
            yield (h1 + index * h2) % self.bit_count

    def add(self, item: str | bytes) -> None:
        for position in self._positions(item):
            self.bits[position // 8] |= 1 << (position % 8)

    def might_contain(self, item: str | bytes) -> bool:
        return all(
            self.bits[position // 8] & (1 << (position % 8))
            for position in self._positions(item)
        )


def perplexity_from_log10_score(log10_probability: float, predicted_token_count: int) -> float:
    """Compute PPL from a log10 joint score and count including EOS if scored."""
    if predicted_token_count <= 0:
        raise ValueError("predicted_token_count must be positive")
    return 10.0 ** (-log10_probability / predicted_token_count)
