# Versioned-tool and evidence-ledger follow-up

Date: 2026-11-22  
Scope: audit of the already merged batch 05 chapters 23–24 and the repository-wide evidence contract.

## Findings

### P1 — DataTrove release drift hidden by an unchanged version string

The chapter previously cited moving `main` while describing DataTrove 0.10.1. At the time of this audit, both the v0.10.1 tag and `main` exposed the package version string `0.10.1`, but their `requires-python` declarations differed:

- Release tag `v0.10.1`: `>=3.10.0`.
- Moving `main` snapshot checked 2026-11-22: `>=3.11`.

This makes the package version string alone insufficient as an immutable source locator. Chapter 23 now pins its code, API, defaults, examples and install command to the v0.10.1 tag, and separately records the dated main-branch observation. The LanguageFilter backend and threshold are explicit in the example.

### P1 — Dolma Toolkit and corpus versions needed separate pins

Chapter 24 now pins CLI behavior to Dolma Toolkit `v1.2.1` and the Dolma 3 repository facts to commit `1a9daced81670e0fa768e47fbed32af6694a1865`. The Dolma Dataset snapshot `v1_7` remains a separate data-version identifier.

### P1 — Dolma document glob and token index metadata

The Toolkit v1.2.1 data-format documentation specifies gzipped JSONL documents under `documents/*/*.jsonl.gz`; the chapter examples now use `*.jsonl.gz`, not `*.json.gz`.

The v1.2.1 tokenization documentation describes metadata CSV columns `start`, `end`, `path` and `id`; the chapter now uses those names rather than the newer/unpinned `src` / `loc` wording.

### P2 — Evidence ledger schema was documented but incompletely enforced

The static validator previously checked only that the ledger existed and that verified claims had a source and locator. It now checks for:
- a non-empty claims list;
- unique claim IDs;
- non-empty claim, kind, source URL, locator, status and notes;
- supported kinds and statuses (including `standard` for RFC/specification claims);
- absolute HTTPS source URLs;
- figure captions and accessible MathML labels in chapters 21–25.

Unit tests enforce the same contract across chapters 01–25.

## Not claimed

- No DataTrove or Dolma pipeline was run against a production corpus.
- No GPU training or benchmark reproduction was performed.
- No browser QA or PDF export is claimed by this follow-up.
- This change does not modify the already published dataset, model weights or course taxonomy.
