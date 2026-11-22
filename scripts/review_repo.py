#!/usr/bin/env python3
"""Cross-chapter semantic and content-integrity audit (stdlib only).

Use alongside scripts/validate_site.py. This script cannot replace browser,
paper-claim, license, training-outcome, or visual SVG inspection.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tag_counts = Counter()
        self.ids = set()
        self.hrefs = []
        self.images = []
        self.range_inputs = []
        self.labels = set()
        self.script_sources = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tag_counts[tag] += 1
        if a.get("id"):
            if a["id"] in self.ids:
                self.errors.append("duplicate_id:" + a["id"])
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "img":
            self.images.append(a)
        if tag == "input" and a.get("type") == "range":
            self.range_inputs.append(a)
        if tag == "label" and a.get("for"):
            self.labels.add(a["for"])
        if tag == "script" and a.get("src"):
            self.script_sources.append(a["src"])


def review(root: Path = ROOT) -> dict:
    catalog = json.loads((root / "courses.json").read_text(encoding="utf-8"))
    pages = {}
    errors = []
    warnings = []
    chapter_ids = {x["num"] for x in catalog["chapters"]}
    assets_used = set()
    category_ids = {x["id"] for x in catalog["categories"]}
    for chapter in catalog["chapters"]:
        num, path = chapter["num"], root / chapter["file"]
        if not path.is_file():
            errors.append(f"{num}: missing HTML")
            continue
        html = path.read_text(encoding="utf-8")
        parser = Inspector()
        parser.feed(html)
        counts = parser.tag_counts
        for issue in parser.errors:
            errors.append(f"{num}: {issue}")
        for tag in ("h1", "main"):
            if counts[tag] != 1:
                errors.append(f"{num}: expected one {tag}, got {counts[tag]}")
        if counts["article"] < 1:
            errors.append(f"{num}: missing article content")
        if counts["nav"] < 1:
            errors.append(f"{num}: missing nav")
        if counts["figure"] != counts["figcaption"]:
            errors.append(f"{num}: uncaptioned figure(s)")
        if counts["figure"] == 0:
            errors.append(f"{num}: no diagrams")
        if chapter.get("status") != "refined":
            errors.append(f"{num}: metadata status is not refined")
        if chapter.get("category") not in category_ids:
            errors.append(f"{num}: unknown category")
        if len(chapter.get("tags", [])) != len(set(chapter.get("tags", []))):
            errors.append(f"{num}: duplicate tag in chapter")
        for p in chapter.get("prerequisites", []):
            if p not in chapter_ids or int(p) >= int(num):
                errors.append(f"{num}: invalid prerequisite {p}")
        if not (root / "evidence" / (num + ".json")).is_file():
            errors.append(f"{num}: missing evidence ledger")
        if ("<h1>" + chapter["title"] + "</h1>") not in html:
            # Older edited headings may be intentionally more descriptive.
            warnings.append(f"{num}: article H1 differs from canonical catalog title")
        if f'href="{num}.html" aria-current="page"' not in html:
            warnings.append(f"{num}: no aria-current in chapter navigation")
        for image in parser.images:
            if not image.get("alt", "").strip():
                errors.append(f"{num}: image missing alt")
            src = image.get("src", "")
            if src.startswith("assets/diagrams/"):
                assets_used.add(src)
        for item in parser.range_inputs:
            input_id = item.get("id", "")
            if not input_id or input_id not in parser.labels:
                warnings.append(f"{num}: range input missing associated label ({input_id})")
        for href in parser.hrefs:
            if href.lower().startswith("javascript:"):
                errors.append(f"{num}: javascript: navigation link")
            if href.startswith("http://"):
                warnings.append(f"{num}: external HTTP link (not HTTPS): {href}")
            if href.startswith("#") and href != "#" and href[1:] not in parser.ids:
                warnings.append(f"{num}: unresolved internal fragment: {href}")
        pages[num] = {"h1": counts["h1"], "main": counts["main"],
                      "figures": counts["figure"], "math": counts["math"],
                      "range_controls": len(parser.range_inputs),
                      "evidence": True}
    diagram_dir = root / "assets" / "diagrams"
    diagrams = sorted(p.relative_to(root).as_posix() for p in diagram_dir.glob("*.svg"))
    orphan = [path for path in diagrams if path not in assets_used]
    if orphan:
        warnings.append(f"{len(orphan)} unreferenced SVG diagrams (listed in report)")
    tags = {tag for c in catalog["chapters"] for tag in c.get("tags", [])}
    return {"chapters": len(pages), "categories": len(catalog["categories"]),
            "tags": len(tags), "diagrams": len(diagrams),
            "referenced_diagrams": len(assets_used), "unreferenced_diagrams": orphan,
            "pages": pages, "errors": errors, "warnings": warnings,
            "limitations": ["No Chromium screenshots or interaction execution",
                            "External links and paper results are not independently fetched",
                            "Rights/privacy review flags are not evidence of actual clearance"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = review()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"REVIEW: {report['chapters']} chapters, {report['diagrams']} diagrams, "
              f"{report['referenced_diagrams']} referenced, {report['tags']} distinct tags; "
              f"{len(report['errors'])} errors, {len(report['warnings'])} warnings.")
        for issue in report["errors"]:
            print("ERROR: " + issue)
        for issue in report["warnings"]:
            print("WARN: " + issue)
    if args.strict and report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
