# AGENTS.md — LLM Data Tutorial

This file is the mandatory operating contract for every contributor and coding agent working in this repository.

## Mission

Build an evidence-grounded, graduate-level learning system for LLM pretraining data engineering. The output is an independently useful technical article and a reliable static knowledge base—not a slide deck, marketing page, or a collection of unverified claims.

Use the pedagogical workflow from Olah-style-posts/skills/olah-style-paper-posts/SKILL.md as the reference method:
- progressive explanation: reader misconception → concrete problem → minimal diagram → mechanism → evidence → limitations;
- annotated implementation: explain code in the order the data actually flows;
- original, semantically accurate SVGs;
- executable or inspectable examples;
- static, responsive, accessible HTML.

Do not copy the reference skill's prose, graphics, CSS, logos, or example assets. Apply the method to data engineering topics.

## Repository invariants

1. courses.json is the canonical source for all chapter metadata.
2. courses-data.js is a generated offline projection. Never hand-edit it independently.
3. Keep the public chapter entry points 01.html–28.html stable unless a migration explicitly updates all references.
4. New article content belongs in its numbered chapter file; diagrams belong in assets/diagrams/; factual claim ledgers belong in evidence/.
5. Keep shared presentation in theme.css. Avoid duplicating large inline style blocks.
6. Every article must be understandable without JavaScript. Interactions are progressive enhancement.
7. Production notes, toolchain boasts, “AI-generated” notes and style imitation claims do not belong in article hero, byline or footer.

## Mandatory workflow

### Gate 0 — Inspect before editing
- Read this file, README, relevant chapter, courses.json, adjacent chapters, and existing tests.
- Check current GitHub branch and default branch before writing.
- Preserve existing content outside the requested scope.

### Gate 1 — Research and evidence ledger
- Prefer primary papers, official documentation, standards, and maintained source repositories.
- Read the relevant method, experiment setup, appendix and limitations—not only abstracts.
- For each factual or quantitative claim, record: claim ID, exact statement, source URL, paper version, section/table/figure/line locator, evidence status and notes.
- verified means directly supported; derived means transparently calculated; illustrative means synthetic teaching data; unverified must not be presented as fact.
- Never invent benchmark values, dataset sizes, throughput, percentages, thresholds, author conclusions or API behavior.
- Separate paper results, implementation behavior, engineering recommendations and teaching simplifications.

### Gate 2 — Plan the learning path
For each article write a short map:
reader question → prior misconception → concrete example → diagram question → mechanism → equation / data shape → runnable example → evidence → failure modes.
Each figure must answer one question and have a caption before it is drawn.

### Gate 3 — Author technical content
- Use one H1; ordered H2/H3 hierarchy; semantic main, article, nav, section, figure, figcaption.
- Explain the exact input/output contract and the assumptions of every code example.
- For math, use semantic MathML with accessible descriptions; never fake a substantive formula with Unicode-only text.
- Label toy data and synthetic scores visibly.
- Keep the article's static content complete if JavaScript fails or is disabled.

### Gate 4 — Draw and verify diagrams
- Draw original SVGs; include viewBox, title, desc, accessible name and unique IDs.
- Diagram topology must match the dataflow described in the article.
- Use color consistently within a diagram, but never rely on color alone.
- Keep labels readable on 360px mobile and in print.
- Do not use external images or remote fonts as a substitute for original explanatory figures.

### Gate 5 — Update knowledge architecture
- Add or update category and tag metadata in courses.json.
- Keep tags orthogonal: category = primary knowledge domain; tags = cross-cutting concepts, methods, data formats, papers and tools.
- Update homepage filters and README only when metadata changes require it.
- Preserve offline operation; no mandatory CDN, API or remote runtime dependency.

### Gate 6 — Validate
Run:
    python3 scripts/build_course_data.py --check
    python3 scripts/validate_site.py
    python3 -m unittest discover -s tests -v
    node --test tests/offline-catalog.test.cjs

For visual or interaction changes, run browser QA at 1440×900, 768×1024, 390×844 and 360×800, plus print mode and network-disabled mode. Record screenshots/reports when tooling is available. If browser QA cannot run, report not verified; never call static parsing a browser test.

### Gate 7 — Review and publish
- Inspect every changed path and generated file.
- Review the diff for unsupported claims, dead links, invalid HTML, SVG errors, accessibility regressions, mobile overflow and stale navigation.
- Prefer a focused branch and PR. Check CI status and changed files before merging.
- Verify the default-branch files after merge. GitHub Pages is only live after the deployment workflow and published URL are checked.

## Topic-specific editorial rules

### Data sources
Distinguish a crawl snapshot, archive format, index, raw response, extracted text and final training dataset. Public availability is not completeness or permission to redistribute.

### Extraction and language
Do not treat tag stripping as main-content extraction. Do not treat classifier scores as calibrated probabilities unless calibration is measured. Keep short, mixed-language and low-resource cases visible in evaluation.

### Filtering and deduplication
A threshold is an experimental choice tied to a dataset and target. Report false-positive risk, retained distribution and downstream evaluation. Do not transfer C4/FineWeb settings as universal defaults.

### Quality and data mixing
“High quality” is task-dependent. Report model, dataset, token budget, tokenizer, evaluation protocol and source locator for any model result. Keep document counts distinct from token counts.

## Completion report

A release report must include:
- changed files and purpose;
- primary sources consulted;
- claims corrected or removed;
- tests actually executed and their results;
- browser sizes/interactions verified or explicitly not verified;
- branch, commit, PR and merge status;
- deployment status only if independently checked.
