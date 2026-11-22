#!/usr/bin/env python3
"""Static checks for the LLM Data Tutorial site; no third-party packages required."""
from __future__ import annotations
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = re.compile(r"^(?:https?:|mailto:|tel:|data:|javascript:)", re.I)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.links = []
        self.ids = set()
        self.stack = []
        self.h1 = 0
        self.figures = 0
        self.figcaptions = 0
        self.main = 0
        self.nav = 0
        self.math = 0
        self.svg = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append(f"duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag in {"a", "img", "script", "link"}:
            value = attrs.get("href") or attrs.get("src")
            if value:
                self.links.append(value)
        if tag == "h1": self.h1 += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.figcaptions += 1
        if tag == "main": self.main += 1
        if tag == "nav": self.nav += 1
        if tag == "math": self.math += 1
        if tag == "svg": self.svg += 1
        if tag == "svg": self.stack.append("svg")
        elif tag == "math": self.stack.append("math")
        elif tag not in {"meta", "link", "img", "input", "br", "hr", "source", "area", "wbr"}:
            self.stack.append(tag)
        if tag == "math" and "svg" in self.stack[:-1]:
            self.errors.append("MathML nested inside SVG")

    def handle_endtag(self, tag):
        if tag in self.stack:
            index = len(self.stack) - 1 - self.stack[::-1].index(tag)
            del self.stack[index:]


def validate():
    errors = []
    data = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
    chapters = data.get("chapters", [])
    if len(chapters) != data.get("chapterCount"):
        errors.append("chapterCount does not match chapter list")
    category_ids = {item["id"] for item in data.get("categories", [])}
    for index, chapter in enumerate(chapters, 1):
        expected = f"{index:02d}"
        if chapter.get("num") != expected: errors.append(f"chapter order mismatch: {expected}")
        if chapter.get("category") not in category_ids: errors.append(f"{expected}: invalid category")
        if not (ROOT / chapter.get("file", "")).is_file(): errors.append(f"{expected}: missing chapter file")
    for chapter in chapters:
        path = ROOT / chapter["file"]
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for link in parser.links:
            if EXTERNAL.match(link) or link.startswith("#") or not link:
                continue
            target = link.split("#", 1)[0].split("?", 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(f"{chapter['file']}: missing local asset/link {target}")
        errors.extend(f"{chapter['file']}: {error}" for error in parser.errors)
        article_text = path.read_text(encoding="utf-8")
        if chapter["num"] in {"16", "17", "18", "19", "20"}:
            if chr(92) + "(" in article_text or chr(92) + ")" in article_text:
                errors.append(f"{chapter['file']}: raw TeX delimiter found without a TeX renderer")
        if chapter["num"] in {f"{n:02d}" for n in range(1, 26)}:
            if parser.h1 != 1: errors.append(f"{chapter['file']}: expected one H1, got {parser.h1}")
            if parser.main != 1: errors.append(f"{chapter['file']}: expected one main, got {parser.main}")
            if parser.nav < 1: errors.append(f"{chapter['file']}: missing nav")
            if parser.figures < 1: errors.append(f"{chapter['file']}: missing figure")
            evidence_path = ROOT / "evidence" / f"{chapter['num']}.json"
            if not evidence_path.is_file():
                errors.append(f"{chapter['file']}: missing evidence ledger")
            else:
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
                if evidence.get("chapter") != chapter["num"]:
                    errors.append(f"{chapter['file']}: evidence chapter number mismatch")
                claims = evidence.get("claims")
                if not isinstance(claims, list) or not claims:
                    errors.append(f"{chapter['file']}: evidence ledger must contain a non-empty claims list")
                    claims = []
                seen_claim_ids = set()
                allowed_kinds = {"paper-result", "paper-method", "official-doc", "implementation", "derived", "illustrative"}
                allowed_statuses = {"verified", "derived", "illustrative", "unverified"}
                required_fields = ("id", "claim", "kind", "source_url", "locator", "status", "notes")
                for claim in claims:
                    if not isinstance(claim, dict):
                        errors.append(f"{chapter['file']}: evidence claim must be an object")
                        continue
                    missing = [field for field in required_fields if not isinstance(claim.get(field), str) or not claim[field].strip()]
                    if missing:
                        errors.append(f"{chapter['file']}: evidence claim missing {', '.join(missing)}")
                    claim_id = claim.get("id")
                    if isinstance(claim_id, str) and claim_id:
                        if claim_id in seen_claim_ids:
                            errors.append(f"{chapter['file']}: duplicate evidence claim id {claim_id}")
                        seen_claim_ids.add(claim_id)
                    if claim.get("kind") not in allowed_kinds:
                        errors.append(f"{chapter['file']}: unsupported evidence kind {claim.get('kind')!r}")
                    if claim.get("status") not in allowed_statuses:
                        errors.append(f"{chapter['file']}: unsupported evidence status {claim.get('status')!r}")
                    source_url = claim.get("source_url", "")
                    parsed = urlparse(source_url) if isinstance(source_url, str) else None
                    if not parsed or parsed.scheme != "https" or not parsed.netloc:
                        errors.append(f"{chapter['file']}: evidence source_url must be absolute HTTPS ({claim_id})")
                    if claim.get("status") == "verified" and not (claim.get("source_url") and claim.get("locator")):
                        errors.append(f"{chapter['file']}: verified claim missing source/locator: {claim_id}")
                if chapter["num"] in {f"{n:02d}" for n in range(21, 26)}:
                    if parser.figures != parser.figcaptions:
                        errors.append(f"{chapter['file']}: every figure must have a figcaption")
                    for tag, attrs in parser.tags:
                        if tag == "math" and not attrs.get("aria-label"):
                            errors.append(f"{chapter['file']}: MathML element missing aria-label")
    svg_dir = ROOT / "assets" / "diagrams"
    for svg_path in sorted(svg_dir.glob("*.svg")):
        try:
            root = ET.parse(svg_path).getroot()
            if root.tag.split("}")[-1] != "svg": errors.append(f"{svg_path}: root is not svg")
            if not root.attrib.get("viewBox"): errors.append(f"{svg_path}: missing viewBox")
            if not any(child.tag.split("}")[-1] == "title" for child in root): errors.append(f"{svg_path}: missing title")
            if not any(child.tag.split("}")[-1] == "desc" for child in root): errors.append(f"{svg_path}: missing desc")
            ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
            if len(ids) != len(set(ids)): errors.append(f"{svg_path}: duplicate SVG id")
        except ET.ParseError as exc:
            errors.append(f"{svg_path}: invalid XML: {exc}")
    if errors:
        print("FAIL")
        for error in errors: print(" - " + error)
        return 1
    print(f"PASS: {len(chapters)} chapters, {len(list(svg_dir.glob('*.svg')))} SVG diagrams, metadata and links checked.")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
