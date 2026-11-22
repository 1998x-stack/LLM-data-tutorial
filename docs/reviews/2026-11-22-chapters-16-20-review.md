# Chapters 16–20 quality review — 2026-11-22

## Scope

Reviewed the existing chapter files (16–20), their evidence ledgers, course metadata, implementation modules and associated tests. These chapters already exist on `main`; this review does not recreate or duplicate them.

External source spot-checks were performed for the claims with the highest numerical or methodological impact, including DCLM, the NeurIPS 2025 cross-lingual tokenizer study, and TokLens (ACL 2026 SRW).

## Chapter-by-chapter result

| Chapter | Review focus | Result | Action |
|---|---|---|---|
| 16 — 大规模数据存储 | Parquet row-group / column-chunk / page hierarchy; Arrow vs Parquet; Iceberg snapshots/manifests; S3 object consistency; Dolma scale claim | No critical factual mismatch found in the inspected claims. The article correctly distinguishes object-level consistency from multi-object transactions and marks compression ratio as a measured input. | No content rewrite. Preserve the measured-ratio caveat. |
| 17 — 流水线可复现性 | DVC stage invalidation and lock files; Iceberg snapshots; run identity; canonical serialization; shard manifest digest | Found a maintainability and portability gap: the article's inline implementation had drifted from the tested `scripts/repro_manifest.py` helper and did not show the helper's path/checksum/row-count validation. The name “canonical JSON” could also be mistaken for cross-language RFC 8785/JCS conformance. | Align the chapter with the tested helper, reject ambiguous Windows/backslash/NUL paths, add regression tests, and explicitly document the project-local serialization boundary. |
| 18 — 数据质量评估体系 | DCLM experimental scale/results; Dolma corpus description; simple-random-sample planning; Wilson interval | Inspected claims retain their experiment scope. The sample-size formula is presented as a simple-random-sampling planning approximation, not a substitute for stratification, clustering or nonresponse adjustments. | No content rewrite. Keep the design-effect and sampling caveats visible. |
| 19 — Tokenization 与 BPE | BPE pair-frequency merges; character-level teaching implementation vs byte-level BPE; SentencePiece; tiktoken; cross-language compression measurement | The chapter distinguishes the simplified character-BPE teaching model from production byte-level tokenizer pipelines. The cited NeurIPS 2025 result is framed as a cross-language token-premium study, not as a universal tokenizer ranking. | No content rewrite. Preserve the distinction between bytes/token within one language and parallel-text token-premium comparisons. |
| 20 — 词表设计与优化 | Embedding / LM-head parameter arithmetic; tied vs untied weights; vocabulary-size trade-offs; NeurIPS 2025 and TokLens evidence | The inspected evidence supports the scoped claims. The article does not treat 128K as a universal optimum and distinguishes correlational multilingual findings from causal guarantees. | No content rewrite. Preserve the statement that vocabulary size is a joint model/data/system trade-off. |

## Changes in this review branch

1. `scripts/repro_manifest.py`: reject backslashes, Windows drive prefixes and embedded NUL characters in shard paths so that a manifest path has one portable POSIX interpretation.
2. `tests/test_repro_manifest.py`: add regression cases for backslash paths, drive-prefixed paths, UNC-style paths and embedded NUL.
3. `17.html`: replace the stale inline implementation with an example that calls the tested repository helper.
4. `17.html` and `evidence/17.json`: clarify that the helper defines a project-local stable serialization contract and is not automatically RFC 8785/JCS.
5. Add the RFC 8785 reference and this five-chapter review record.

## External source checks

- DCLM paper / official research summary: https://arxiv.org/abs/2406.11794 and https://machinelearning.apple.com/research/datacomp-lm-search
- Dolma ACL 2024: https://aclanthology.org/2024.acl-long.840/
- NeurIPS 2025, *Explaining and Mitigating Crosslingual Tokenizer Inequities*: https://proceedings.neurips.cc/paper_files/paper/2025/file/5b91cefbfa52340af2f16f249572dc76-Paper-Conference.pdf
- TokLens, ACL 2026 SRW: https://aclanthology.org/2026.acl-srw.18/
- RFC 8785, JSON Canonicalization Scheme: https://www.rfc-editor.org/rfc/rfc8785

## Validation status

The branch is awaiting GitHub Actions. This file records the editorial/source review; it does not claim that the new regression tests, full site build, browser QA or deployment have passed. Those states will be updated only from the corresponding workflow results.
