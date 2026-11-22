# Portfolio Engineering Improvements

### 2026-11-05 08:15 UTC — ChatGPT Portfolio Iteration
- Run ID: 20261105T081325Z-llmdata-6d2f
- Repo / Base SHA: 1998x-stack/LLM-data-tutorial / eca884f1bd671e885b2969a47eca4401a3880362
- Historical context: docs/improvements.md returned GitHub 404 on main before any modification; no previous improvement entries or PRs were found. First initialization; no older history to modify.
- Product problem & expected user value: README promises zero-install opening of index.html, but fetch('courses.json') may fail under file://. Restore 28-chapter offline discovery for first-time learners.
- Engineering diagnosis & evidence: index.html inline script depends on JSON fetch; footer and error states used innerHTML and manifest URLs were unchecked. Source-level evidence and V8 offline DOM reproduction.
- Options & decision: Offline first-use repair P1 score 16 (benefit 5 + correctness 4 + evidence 5 + verifiability 5 - cost 2 - risk 1); chapter search P2 score 9; mobile navigation P2 score 7. Only offline repair implemented.
- Changes: index.html now reads synchronous local courses-data.js and validates NN.html links, uses textContent for errors/footer; courses-data.js is generated from canonical courses.json; scripts/build_course_data.py generates/checks projection; tests/offline-catalog.test.cjs covers five cases. No public API or lesson contents changed.
- Validation: A: executed actual GitHub branch index script in V8 simulated DOM, 10/10 assertions passed including 28 cards, local links, missing data, invalid URL, text safety, and JSON projection integrity. C: generator source and Node test source inspected. D: node --test tests/offline-catalog.test.cjs, python3 scripts/build_course_data.py --check, real Chromium file:// and HTTP browser tests not run in full checkout; do not claim passed.
- Security & regression review: Restricts manifest href to local NN.html, avoids dynamic innerHTML; no secrets, production config, workflows, licenses, or deployment changes. Main branch untouched.
- Risk & rollback: Editing courses.json requires regenerating courses-data.js; check mode detects drift. Revert this PR's commits to restore previous behavior. Physical browser compatibility remains unverified.
- Follow-up: Run real Chromium file:// and HTTP E2E and confirm generator --check and Node test suite.
- Commit: 3c1812baa7017dcf93303cd1f72e04deddea3365 (initial iteration record; follow-up metadata commit follows)
- PR: https://github.com/1998x-stack/LLM-data-tutorial/pull/1


### 2026-11-21 — Batch 04: storage, reproducibility, quality, tokenization and vocabulary
- Scope: migrate chapters 16–20 to the evidence-backed Olah-style article system while preserving stable URLs.
- Content: Parquet / Arrow / Iceberg; DVC / run manifests; DCLM / Dolma / dataset datasheets; BPE / SentencePiece / tiktoken; vocabulary matrix and multilingual token-premium analysis.
- Assets: ten original SVGs, five evidence ledgers, five accessible interactive exercises, five dependency-free utility modules and 24 unit tests.
- Editorial controls: no universal storage sizing, no seed-only reproducibility claim, no one-number data-quality score, no conflation of teaching BPE with production byte-level BPE, no universally optimal vocabulary size.
- **Validation / publication:** PR #5 merged; static CI passed (45 Python tests, 10 Node tests, 28 chapter paths and 34 SVGs validated); GitHub Pages deployment succeeded. Browser screenshot QA was not run in this batch.


### 2026-11-22 — Batch 05: synthetic data, domain adaptation, DataTrove, Dolma and cleaning paradigms
- Migrated chapters 21–25 to the evidence-backed article system with 14 original SVG diagrams, five source-located evidence ledgers, five interactive exercises and five dependency-free utility modules.
- Replaced legacy unsupported market-share / model-collapse percentages, unverified DataEvolver claims and anecdotal domain-adaptation numbers with primary-paper or official-document evidence and explicit scope notes.
- Added tests for sequential synthetic-data attrition, token-mixture arithmetic, DataTrove task planning, Bloom-filter sizing and precision/recall/F1.
- Updated the course catalog, homepage count, taxonomy, architecture, AGENTS.md, article-authoring and quality gates.
- **Publication:** PR #7 merged; static CI passed (62 Python tests, 12 Node tests; 28 chapters and 48 SVGs validated); GitHub Pages build and deployment succeeded. Browser screenshot QA was not run in this batch.


### 2026-11-22 — Final batch 06: 26–28 and repository-wide review
- New research-grounded chapters cover agentic data preparation, static/offline/online mixture methods, and a runnable stdlib corpus capstone.
- Added 9 original SVGs, 3 source-located evidence ledgers, 3 interactive exercises, deterministic Python gate/mixer/capstone helpers and tests.
- Replaced unsupported DataEvolver claims, fixed schedule myths and fictitious DataTrove API usage in legacy 26–28 articles.
- Extended catalog and site quality gates to 28/28. Full review and final CI/Pages status recorded in docs/reviews/2026-11-22-full-repository-review.md after verification.
