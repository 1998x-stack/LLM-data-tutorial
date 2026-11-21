# Repository architecture

## Design goals

- Preserve stable, directly addressable chapter URLs.
- Separate content, catalog metadata, visual assets, evidence and validation tooling.
- Keep the site static and offline-first.
- Make category/tag discovery a first-class part of the homepage.
- Permit gradual migration: chapters 01–15 use the new article system; chapters 16–28 retain legacy markup until each is reviewed.

## Source-of-truth boundaries

| Concern | Canonical location | Generated / derived location |
|---|---|---|
| Chapter title, category, tags, level, prerequisites | courses.json | courses-data.js |
| Article narrative and examples | NN.html | none |
| Diagram geometry | assets/diagrams/*.svg | referenced by article |
| Factual claims and source locators | evidence/NN.json | article references |
| Shared CSS | theme.css | browser rendering |
| Workflow rules | AGENTS.md, docs/*.md | contributor behavior |
| Validation | scripts/, tests/ | CI results |

## Directory contract

- Root 01.html–28.html: stable public chapter URLs.
- assets/diagrams/: standalone original SVGs. Filenames include chapter number and concept.
- evidence/: one JSON claim ledger per deeply revised chapter.
- docs/: content model, taxonomy, authoring, source and quality standards.
- scripts/: deterministic build and static validation.
- tests/: offline catalog, HTML, link and evidence checks.
- .github/workflows/: repeatable quality gates.

## Homepage data flow

courses.json → scripts/build_course_data.py → courses-data.js → index.html.

The homepage never fetches JSON at runtime, so file:// browsing works. Search and category/tag filters operate on the generated local object. DOM content is created with textContent and validated local chapter paths; untrusted metadata must never be injected with innerHTML.

## Chapter rendering

Deeply revised chapters 01–15 use theme.css classes:
- article-shell, article-layout, article-toc, article-main;
- article-hero, lead-note, diagram, callout;
- math-scroll, stage-picker, interactive-output;
- article-footer.

Legacy chapters keep double-border, container, sidebar and main-content styles until migration. Do not remove legacy CSS until all 28 chapters are migrated and tested.

## Future migration policy

Migrate one batch at a time. A chapter migration must update the article, evidence ledger, category/tag metadata if needed, diagram assets, tests and navigation. Do not mass-rewrite all legacy pages just to make their markup look uniform.
