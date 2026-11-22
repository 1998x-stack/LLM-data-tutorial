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

## Review method

1. Verify chapter order, categories, statuses and prerequisite DAG.
2. Parse 28 HTML pages for heading/main/nav/article/figures/figcaptions, local SVG references, image alt text and accessible input labels.
3. Validate all SVG XML, viewBox, title/desc and duplicate IDs with scripts/validate_site.py.
4. Validate evidence/01.json through evidence/28.json for source locator, kind, status and claim IDs.
5. Check MathML and interaction hooks on chapters 26–28; compare JS formulas with tested Python helpers.
6. Test capstone deterministic and tamper-resistant artifacts. Static tests do not prove that results improve a real trained model.
7. Compare main and feature branch, check PR/CI and Pages independently.

## Acceptance outcomes

Static CI, PR merge and Pages status will be recorded following the actual checks. Do not infer that passing static HTML checks means actual Chromium/mobile/print QA passed.

## Residual risks / out-of-scope

- **Browser QA not yet verified:** real Chromium screenshots at 1440, 768, 390 and 360px, mobile math, keyboard focus, JS event interaction, print mode, and offline network emulation require execution.
- **Scientific reproduction not attempted:** primary references and scope are cited, but original model training and paper ablations are not reproduced.
- **External links may drift:** reference URLs are source-located but not all were browser-opened.
- **Production rights/PII:** teaching flags do not prove real-world permission, privacy clearance or benchmark decontamination.
- **Scale:** the capstone reads entire small fixtures into memory; production requires WARC parsing, streaming, sharding, retry-safe sinks, cross-crawl dedup and downstream evaluations.
- **Visual SVG QA:** static XML checking is necessary but does not replace independent browser rendering and human topology inspection.
