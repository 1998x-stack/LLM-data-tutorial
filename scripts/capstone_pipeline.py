"""Deterministic, standard-library-only *teaching* corpus pipeline.

Not a WARC extractor, PII detector, legal-review system, tokenizer, fuzzy
scheduler, or production-scale processor. An explicit reviewer must approve
release candidates; no command publishes data remotely.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

CODE_VERSION = "capstone-v1.0"
REQUIRED = ("id", "text", "source", "license", "lang", "rights_reviewed", "privacy_reviewed")


def _json_bytes(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _clean_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).split())


def _policy(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("policy must be an object")
    for key in ("allowed_sources", "allowed_licenses", "allowed_languages", "blocked_ids"):
        if not isinstance(obj.get(key), list) or any(not isinstance(v, str) for v in obj[key]):
            raise ValueError(f"{key} must be an array of strings")
    for key in ("min_chars", "min_accepted"):
        if isinstance(obj.get(key), bool) or not isinstance(obj.get(key), int) or obj[key] < 0:
            raise ValueError(f"{key} must be a non-negative integer")
    ratio = obj.get("max_rejection_fraction")
    if isinstance(ratio, bool) or not isinstance(ratio, (int, float)) or not 0 <= ratio <= 1:
        raise ValueError("max_rejection_fraction must be within [0,1]")
    return obj


def _reject_reason(doc: object, policy: dict, seen_ids: set, seen_text: set) -> tuple[str | None, str | None]:
    if not isinstance(doc, dict):
        return "invalid_schema", None
    if any(key not in doc for key in REQUIRED):
        return "missing_required_field", None
    if any(not isinstance(doc[key], str) or not doc[key].strip() for key in REQUIRED[:5]):
        return "invalid_schema", None
    if type(doc["rights_reviewed"]) is not bool or type(doc["privacy_reviewed"]) is not bool:
        return "invalid_schema", None
    identity = (doc["source"], doc["id"])
    if identity in seen_ids:
        return "duplicate_document_id", None
    seen_ids.add(identity)
    if doc["source"] not in policy["allowed_sources"]:
        return "source_not_allowed", None
    if doc["license"] not in policy["allowed_licenses"]:
        return "license_not_allowed", None
    if not doc["rights_reviewed"]:
        return "rights_review_required", None
    if not doc["privacy_reviewed"]:
        return "privacy_review_required", None
    if doc["id"] in policy["blocked_ids"]:
        return "evaluation_holdout_id", None
    if doc["lang"] not in policy["allowed_languages"]:
        return "language_not_allowed", None
    normalized = _clean_text(doc["text"])
    if len(normalized) < policy["min_chars"]:
        return "too_short", None
    digest = _sha(normalized.encode("utf-8"))
    if digest in seen_text:
        return "duplicate_text", None
    seen_text.add(digest)
    return None, normalized


def verify_release(release_dir: str | Path) -> dict:
    base = Path(release_dir)
    manifest = json.loads((base / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["output_sha256"].items():
        if name not in ("curated.jsonl", "rejected.jsonl", "quality_report.json"):
            raise ValueError("unexpected output file in manifest")
        actual = _sha((base / name).read_bytes())
        if actual != expected:
            raise ValueError(f"checksum mismatch: {name}")
    with (base / "curated.jsonl").open(encoding="utf-8") as handle:
        curated_count = sum(1 for _ in handle)
    with (base / "rejected.jsonl").open(encoding="utf-8") as handle:
        rejected_count = sum(1 for _ in handle)
    if curated_count != manifest["accepted_docs"] or rejected_count != manifest["rejected_docs"]:
        raise ValueError("record counts differ from manifest")
    if curated_count + rejected_count != manifest["input_docs"]:
        raise ValueError("input/output count mismatch")
    return manifest


def build_release(input_path: str | Path, policy_path: str | Path, output_root: str | Path) -> tuple[Path, dict]:
    src, policy_file, root = Path(input_path), Path(policy_path), Path(output_root)
    policy = _policy(policy_file)
    raw = src.read_bytes()
    input_sha, policy_sha = _sha(raw), _sha(_json_bytes(policy))
    run_id = _sha(_json_bytes({"input": input_sha, "policy": policy_sha, "code": CODE_VERSION}))[:24]
    root.mkdir(parents=True, exist_ok=True)
    destination = root / run_id
    if destination.exists():
        old = verify_release(destination)
        if old.get("input_sha256") != input_sha or old.get("policy_sha256") != policy_sha:
            raise ValueError("existing release is incompatible")
        return destination, old

    parsed = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        try:
            obj = json.loads(line.decode("utf-8"))
            parsed.append((line_no, obj, None))
        except (UnicodeDecodeError, json.JSONDecodeError):
            parsed.append((line_no, None, "invalid_json"))
    def sort_key(row):
        ln, obj, _ = row
        if isinstance(obj, dict):
            return (str(obj.get("source", "")), str(obj.get("id", "")), ln)
        return ("", "", ln)
    parsed.sort(key=sort_key)
    seen_ids, seen_text = set(), set()
    kept, rejected = [], []
    by_reason = Counter()
    by_source = Counter()
    for line_no, doc, error in parsed:
        reason, normalized = (error, None) if error else _reject_reason(doc, policy, seen_ids, seen_text)
        source = doc.get("source") if isinstance(doc, dict) and isinstance(doc.get("source"), str) else None
        identity = doc.get("id") if isinstance(doc, dict) and isinstance(doc.get("id"), str) else None
        if reason:
            by_reason[reason] += 1
            # Deliberately omit raw rejected text; may contain sensitive material.
            rejected.append({"line": line_no, "id": identity, "source": source, "reason": reason})
        else:
            by_source[source] += 1
            kept.append({"id": identity, "source": source, "license": doc["license"],
                         "lang": doc["lang"], "text": normalized,
                         "provenance": {"input_line": line_no, "rights_reviewed": True,
                                        "privacy_reviewed": True}})
    n = len(parsed)
    rejection_rate = len(rejected) / n if n else 1.0
    gate = "READY_FOR_HUMAN_APPROVAL" if (len(kept) >= policy["min_accepted"]
        and rejection_rate <= policy["max_rejection_fraction"]) else "HOLD_FOR_REVIEW"
    report = {"input_docs": n, "accepted_docs": len(kept), "rejected_docs": len(rejected),
              "rejection_fraction": rejection_rate, "rejection_reasons": dict(sorted(by_reason.items())),
              "accepted_by_source": dict(sorted(by_source.items())), "gate": gate,
              "limitations": ["exact NFC/whitespace dedup only", "not a PII detector",
                              "rights/privacy_reviewed are upstream assertions", "no tokenizer or downstream training"]}
    outputs = {"curated.jsonl": b"".join(_json_bytes(item) for item in kept),
               "rejected.jsonl": b"".join(_json_bytes(item) for item in rejected),
               "quality_report.json": _json_bytes(report)}
    manifest = {"schema_version": 1, "code_version": CODE_VERSION, "run_id": run_id,
                "input_sha256": input_sha, "policy_sha256": policy_sha,
                "input_docs": n, "accepted_docs": len(kept), "rejected_docs": len(rejected),
                "output_sha256": {name: _sha(value) for name, value in outputs.items()},
                "gate": gate, "remote_publication": "not_performed"}
    stage = Path(tempfile.mkdtemp(prefix=".staging-", dir=root))
    try:
        for name, contents in outputs.items():
            (stage / name).write_bytes(contents)
        (stage / "manifest.json").write_bytes(_json_bytes(manifest))
        # Same-filesystem directory rename; external object stores require different commits.
        if destination.exists():
            raise FileExistsError("concurrent release: retry and verify the existing directory")
        os.rename(stage, destination)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return destination, verify_release(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or verify a local teaching corpus release")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        result = verify_release(args.verify)
        print(json.dumps({"verified": True, "run_id": result["run_id"], "gate": result["gate"]}))
        return
    if not (args.input and args.policy and args.out):
        parser.error("--input, --policy and --out are required unless --verify is given")
    path, manifest = build_release(args.input, args.policy, args.out)
    print(json.dumps({"output": str(path), "gate": manifest["gate"],
                      "accepted_docs": manifest["accepted_docs"],
                      "rejected_docs": manifest["rejected_docs"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
