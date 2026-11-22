# Full-repository review · LLM Data Tutorial · 2026-11-22

## Scope

Repository: https://github.com/1998x-stack/LLM-data-tutorial
Branches: main versus final-batch implementation branch
Reviewed surface: all 28 article paths, catalog, homepage, AGENTS, README, docs, SVG, evidence ledger schema, Python examples, test suite and publishing workflow. External paper claims for the new chapters were cross-checked against primary papers or official documentation; this is not a substitute for a full independent scientific replication.

## Findings fixed in this batch

| Priority | Finding | Action |
|---|---|---|
| P0 | Legacy 28 included non-existent / incompatible DataTrove chained pipeline methods and unspecified filters, implying the example could run | Replaced with an executed, standard-library-only pipeline, fixture, policy, checksum manifest and unit tests; documented scaling gaps |
| P0 | Legacy 26 presented DataEvolver and unverified speedups as factual | Removed. Explained DataFlow and Data-Juicer with primary-source anchors and separated planner sandbox from release control |
| P1 | Legacy 27 treated curriculum schedules as universal and conflated static/proxy learning with online feedback | Rebuilt around DoReMi, RegMix, RegMix-D offline/online, ODM and AC-ODM with specific limits |
| P1 | Chapters 26–28 lacked the evidence-ledger system and semantic article/diagrams/interactive QA | Added three evidence ledgers, nine SVGs, mathematical examples, Python reference code and accessible controls |
| P1 | Catalog and homepage still reflected 25 deeply revised chapters | Updated all 28 statuses, prerequisites, tags, generated local catalog, homepage, README, taxonomy and AGENTS |
| P1 | Site validator only enforced the semantic/evidence rules through chapter 25 | Extended static gating through chapter 28 and added a repository-wide audit script |
| P2 | A data-preparation agent could be confused with a privileged auto-publisher | Explicit independent human-approval gate, immutable checksums, audit trail, and no remote publishing action |
| P2 | Repository-wide scan identified 15 SVG files no longer referenced by any of the 28 chapters (old batch 05 variants plus ch14-mixture-optimization) | Removed all 15 from the active tree, preserving Git history, and enforced zero orphan SVGs in tests |
| P1 | Chromium initially detected table-induced document overflow on mobile in 26–28 | Wrapped five tables in keyboard-focusable horizontal scroll regions; retested 390px and 360px with zero overflow |
| P1 | Slider QA initially showed unchanged outputs for certain choices | Re-tested each input from default state against both endpoints; confirmed every interactive control has meaningful output changes at supported values |

## Review method

1. Verify chapter order, categories, statuses and prerequisite DAG.
2. Parse 28 HTML pages for heading/main/nav/article/figures/figcaptions, local SVG references, image alt text and accessible input labels.
3. Validate all SVG XML, viewBox, title/desc and duplicate IDs with scripts/validate_site.py.
4. Validate evidence/01.json through evidence/28.json for source locator, kind, status and claim IDs.
5. Check MathML and interaction hooks on chapters 26–28; compare JS formulas with tested Python helpers.
6. Test capstone deterministic and tamper-resistant artifacts. Static tests do not prove that results improve a real trained model.
7. Compare main and feature branch, check PR/CI and Pages independently.

## Acceptance outcomes (feature branch)

- **Final reviewed commit:** `109367bcfb728e170e8011b95ac704868fcbf922` on `feat/final-three-and-full-review-20261122`.
- **Final feature-branch workflow:** [Site quality run 45001201332](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/45001201332) — **success**. Python **83/83**, Node **14/14**, catalog generation and structure checks succeeded.
- **Full repository static audit:** 28/28 chapters, 47/47 SVG files referenced and parsed, 206 distinct catalog tags, **0 errors / 0 warnings**. All 28 have evidence ledgers and valid prerequisite metadata.
- **Real Chromium automated QA:** [browser artifact](https://github.com/1998x-stack/LLM-data-tutorial/actions/runs/45001201332/artifacts/14745773119) — **116 page/viewport checks, 0 issues**; index plus 01–28 at 1440×900, 768×1024, 390×844 and 360×800, using offline file URLs. Verified document horizontal overflow, image/SVG load and geometry, MathML namespace and visible geometry, JS page/console errors, figure captions, and 26–28 controls' observable behavior.
- **Captured screenshots:** index and chapters 26, 27, 28 at four viewport sizes (16 images), with machine-readable browser report. This is automated visual evidence, not a claim that every image's artistic composition was manually reviewed.
- **Capstone test fixture:** 12 fictional inputs → 5 accepted + 7 rejected; repeatability, policy changes, tamper verification, and exclusion of rejected raw text covered in tests.
- **New sources:** 30 source-located claims in chapters 26–28. Primary-paper and official-doc cross-checks are not independent reproductions of the original experiments.
- **PR review:** [PR #10](https://github.com/1998x-stack/LLM-data-tutorial/pull/10), merge status and latest main/Pages deployment must be independently recorded after squash merge.

## Residual risks / out-of-scope

- **Browser QA boundary:** automated Chromium file:// tests and screenshots passed at all four viewports. Manual visual topology review of screenshot sets, detailed keyboard tab-order/visible-focus inspection and print emulation were not performed.
- **Scientific reproduction not attempted:** primary references and scope are cited, but original model training and paper ablations are not reproduced.
- **External links may drift:** reference URLs are source-located but not all were browser-opened.
- **Production rights/PII:** teaching flags do not prove real-world permission, privacy clearance or benchmark decontamination.
- **Scale:** the capstone reads entire small fixtures into memory; production requires WARC parsing, streaming, sharding, retry-safe sinks, cross-crawl dedup and downstream evaluations.
- **Visual SVG QA:** Chromium confirmed nonzero image geometry and loaded SVGs, but per-diagram topology and small-label overlap require manual visual inspection.
