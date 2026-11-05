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
- Commit: pending
- PR: pending
