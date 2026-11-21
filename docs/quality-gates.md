# Quality gates and release checklist

## Static gates

- courses.json parses and contains unique chapter numbers and valid category IDs.
- courses-data.js is reproducibly generated from courses.json.
- Every chapter file exists and every local chapter link resolves.
- New articles have one H1, semantic main/article/nav, figure captions and primary references.
- SVG files parse as XML, have viewBox/title/desc and unique IDs.
- MathML is not nested inside SVG; fractions/scripts have correct child arity; display formulas have accessible scroll regions.
- Evidence ledger JSON parses and every verified claim has a source and locator.
- No external CDN is required for page rendering.

## Browser gates

Test at 1440×900, 768×1024, 390×844 and 360×800:
- document width does not exceed viewport;
- navigation, text, tables and diagrams remain readable;
- images/SVGs load and have nonzero geometry;
- no console or page errors;
- keyboard focus is visible;
- every interactive control changes a meaningful state;
- MathML namespace, geometry and fraction layout are checked where present;
- print emulation preserves key diagrams and formulas;
- network-disabled rendering remains functional.

## Release report

Report each check as passed, failed or not verified. Static validation does not prove browser rendering. A successful Git commit does not prove CI, merge or Pages deployment. Verify each separately.
