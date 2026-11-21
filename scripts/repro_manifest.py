"""Canonical identity helpers for reproducible corpus manifests."""
from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON with stable key ordering and no insignificant whitespace."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_digest(value: Any) -> str:
    return sha256_hex(canonical_json_bytes(value))


def dataset_root_digest(shards: list[dict]) -> str:
    """Hash a stable, sorted shard manifest; this is not a Merkle tree."""
    normalized = []
    seen_paths = set()
    for shard in shards:
        path = str(PurePosixPath(shard["path"]))
        if path in {"", "."} or path.startswith("/") or ".." in PurePosixPath(path).parts:
            raise ValueError("shard path must be a safe relative POSIX path")
        if path in seen_paths:
            raise ValueError(f"duplicate shard path: {path}")
        seen_paths.add(path)
        digest = str(shard["sha256"]).lower()
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ValueError("sha256 must be 64 hexadecimal characters")
        rows = shard["rows"]
        if isinstance(rows, bool) or not isinstance(rows, int) or rows < 0:
            raise ValueError("rows must be a non-negative integer")
        normalized.append({"path": path, "sha256": digest, "rows": rows})
    normalized.sort(key=lambda item: item["path"])
    return canonical_json_digest({"shards": normalized})
