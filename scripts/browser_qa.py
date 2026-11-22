#!/usr/bin/env python3
"""Chromium read-only QA for all 28 static articles, homepage and 26–28 demos.

Run after: python -m pip install playwright && python -m playwright install chromium
All navigation uses local file:// URLs and browser offline mode. Produces actual
desktop/mobile screenshots and a machine-readable JSON report; failures are
reported, not silently ignored. Does not certify academic or legal accuracy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWS = (
    ("desktop", 1440, 900),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
    ("narrow", 360, 800),
)
SCREENSHOT_PAGES = {"index", "26", "27", "28"}


def run(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    checks, issues = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for view, width, height in VIEWS:
            context = browser.new_context(viewport={"width": width, "height": height},
                                          reduced_motion="reduce", service_workers="block")
            context.set_offline(True)
            for number in ["index"] + [f"{i:02d}" for i in range(1, 29)]:
                page = context.new_page()
                filename = number + ".html"
                path = ROOT / filename
                errors = []
                console_errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
                try:
                    page.goto(path.as_uri(), wait_until="load", timeout=20_000)
                    page.wait_for_timeout(20)
                    result = page.evaluate("""() => ({
                      viewport: window.innerWidth,
                      documentWidth: document.documentElement.scrollWidth,
                      bodyWidth: document.body.scrollWidth,
                      images: Array.from(document.images).map(i => ({
                        src: i.getAttribute('src'),
                        loaded: i.complete && i.naturalWidth > 0,
                        width: i.getBoundingClientRect().width,
                        height: i.getBoundingClientRect().height
                      })),
                      math: Array.from(document.querySelectorAll('math')).map(el => ({
                        namespace: el.namespaceURI,
                        width: el.getBoundingClientRect().width,
                        height: el.getBoundingClientRect().height
                      })),
                      figures: Array.from(document.querySelectorAll('figure')).map(el => ({
                        height: el.getBoundingClientRect().height,
                        caption: !!el.querySelector('figcaption')
                      }))
                    })""")
                    bad = []
                    if result["documentWidth"] > result["viewport"] + 2:
                        bad.append(f"horizontal_overflow:{result['documentWidth']}>{result['viewport']}")
                    for img in result["images"]:
                        if not img["loaded"] or img["width"] <= 0 or img["height"] <= 0:
                            bad.append(f"broken_image:{img['src']}")
                    for math in result["math"]:
                        if math["namespace"] != "http://www.w3.org/1998/Math/MathML":
                            bad.append("invalid_math_namespace")
                        if math["width"] <= 0 or math["height"] <= 0:
                            bad.append("invisible_math")
                    for fig in result["figures"]:
                        if fig["height"] <= 0 or not fig["caption"]:
                            bad.append("figure_missing_geometry_or_caption")
                    if number in {"26", "27", "28"}:
                        for ctl in page.locator('input[type="range"]').all():
                            cid = ctl.get_attribute("id")
                            if not cid or not page.locator(f'label[for="{cid}"]').count():
                                bad.append("missing_range_label:" + str(cid))
                                continue
                            before = page.locator('[aria-live="polite"]').first.inner_text()
                            ctl.evaluate("""el => {
                              let next = el.value === el.min ? el.max : el.min;
                              el.value = next;
                              el.dispatchEvent(new Event('input', {bubbles:true}));
                            }""")
                            after = page.locator('[aria-live="polite"]').first.inner_text()
                            if before == after:
                                bad.append("inert_range_control:" + cid)
                    if number in SCREENSHOT_PAGES:
                        page.screenshot(path=str(out / f"{number}-{view}.png"),
                                        full_page=True, animations="disabled")
                    bad.extend("pageerror:" + message for message in errors)
                    bad.extend("console:" + message for message in console_errors)
                    checks.append({"page": number, "view": view, "issues": bad,
                                   "diagram_count": len(result["images"]),
                                   "math_count": len(result["math"])})
                    issues.extend(f"{number}@{view}: {error}" for error in bad)
                except Exception as exc:
                    issues.append(f"{number}@{view}: navigation/inspection failed: {exc}")
                    checks.append({"page": number, "view": view, "issues": [str(exc)]})
                finally:
                    page.close()
            context.close()
        browser.close()
    report = {"pages": 29, "viewports": [item[0] for item in VIEWS],
              "checks": len(checks), "failed_checks": len(issues),
              "issues": issues, "results": checks,
              "limitations": ["No training, academic replication, external-link live check, or rights/privacy verification",
                              "Human visual review of screenshot topology remains separate"]}
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
    print(f"BROWSER QA: {report['checks']} page/viewport checks; {len(issues)} issues")
    for item in issues:
        print("FAIL:", item)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("browser-results"))
    args = parser.parse_args()
    result = run(args.out)
    raise SystemExit(bool(result["failed_checks"]))
