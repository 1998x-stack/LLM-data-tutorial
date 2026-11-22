#!/usr/bin/env python3
"""Verify GitHub Pages serves the exact content from the validated main commit."""
from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "index.html",
    "courses.json",
    "courses-data.js",
    "17.html",
    "21.html",
    "22.html",
    "23.html",
    "24.html",
    "25.html",
    "26.html",
    "27.html",
    "28.html",
    "assets/diagrams/ch21-synthetic-data-loop.svg",
    "assets/diagrams/ch23-datatrove-pipeline.svg",
    "assets/diagrams/ch25-curation-paradigms.svg",
    "assets/diagrams/ch26-asset-dag.svg",
    "assets/diagrams/ch27-three-regimes.svg",
    "assets/diagrams/ch28-capstone-pipeline.svg",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "llm-data-pages-qa/1.0", "Cache-Control": "no-cache"})
    with urlopen(req, timeout=25) as response:
        if response.status != 200:
            raise AssertionError(f"Unexpected status {response.status}: {url}")
        return response.read()


def verify(base: str, attempts: int, interval: int) -> None:
    if not base.startswith("https://"):
        raise ValueError("Expected an HTTPS Pages URL")
    for relative in REQUIRED:
        local = ROOT / relative
        if not local.is_file():
            raise AssertionError(f"Local release file missing: {local}")
        expected = local.read_bytes()
        url = urljoin(base, relative)
        last_error: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                actual = fetch(url)
                if not actual:
                    raise AssertionError(f"Empty published asset: {url}")
                if actual != expected:
                    raise AssertionError(
                        f"Stale or mismatched published bytes for {relative}: "
                        f"expected sha256={digest(expected)}, actual sha256={digest(actual)}"
                    )
                print(f"PUBLIC OK {relative}: {len(actual)} bytes, sha256={digest(actual)}", flush=True)
                break
            except (HTTPError, URLError, TimeoutError, AssertionError) as exc:
                last_error = exc
                if attempt == attempts:
                    raise AssertionError(
                        f"Public deployment did not match checked-out commit after {attempts} checks: {relative}"
                    ) from last_error
                print(f"Public check {attempt}/{attempts} for {relative}: {exc}", flush=True)
                time.sleep(interval)
    print(f"PUBLIC DEPLOYMENT VERIFIED: {base}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--attempts", type=int, default=18)
    parser.add_argument("--interval", type=int, default=10)
    args = parser.parse_args()
    if args.attempts < 1 or args.interval < 0:
        parser.error("attempts must be >=1 and interval >=0")
    verify(args.base_url.rstrip("/") + "/", args.attempts, args.interval)


if __name__ == "__main__":
    main()
