#!/usr/bin/env python3
"""Generate the offline browser catalog from courses.json."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "courses.json"
TARGET = ROOT / "courses-data.js"


def build():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    chapters = data.get("chapters")
    categories = data.get("categories")
    if not isinstance(chapters, list) or len(chapters) != data.get("chapterCount"):
        raise ValueError("chapterCount must match the chapters array")
    if not isinstance(categories, list) or not categories:
        raise ValueError("categories must be a non-empty list")
    category_ids = [item.get("id") for item in categories]
    if len(category_ids) != len(set(category_ids)):
        raise ValueError("category IDs must be unique")
    valid_categories = set(category_ids)
    seen_tags = set()
    for index, chapter in enumerate(chapters, 1):
        number = f"{index:02d}"
        if chapter.get("num") != number or chapter.get("file") != number + ".html":
            raise ValueError(f"invalid chapter at position {index}")
        if chapter.get("category") not in valid_categories:
            raise ValueError(f"invalid category for chapter {number}")
        if not isinstance(chapter.get("tags"), list) or not chapter["tags"]:
            raise ValueError(f"chapter {number} needs at least one tag")
        if not isinstance(chapter.get("summary"), str) or not chapter["summary"].strip():
            raise ValueError(f"chapter {number} needs a summary")
        if not (ROOT / chapter["file"]).is_file():
            raise ValueError(f"missing chapter: {chapter['file']}")
        seen_tags.update(chapter["tags"])
    return (
        "/* Generated from courses.json. Run python3 scripts/build_course_data.py. */\n"
        + "window.COURSE_CATALOG = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != expected:
            parser.error("courses-data.js is stale; regenerate it")
    else:
        TARGET.write_text(expected, encoding="utf-8")


if __name__ == "__main__":
    main()
