# Quality gates and release checklist

## Static gates

- courses.json parses and contains unique chapter numbers and valid category IDs.
- courses-data.js is reproducibly generated from courses.json.
- Every chapter file exists and every local chapter link resolves.
- New articles 01–25 have one H1, semantic main/article/nav, figure captions, accessible MathML and primary references.
- Algorithm examples have dependency-free unit tests for URL semantics, Bloom parameters, Jaccard, LSH candidate probability, perplexity score conversion, document-to-token mixture math, storage capacity estimates, manifest fingerprints, Wilson intervals, BPE merges, vocabulary parameter costs, synthetic-data attrition, domain token mixtures, task-sharding estimates, Bloom-filter sizing and cleaning confusion-matrix metrics.
- Articles 11–15 distinguish synthetic teaching values from empirical paper results and include source locators for verified quantitative claims.
- Annotation exercises state that LLM labels are noisy measurements; contamination detection separates overlap from task leakage; data-mixture examples distinguish document shares from token shares.
- Distributed-processing examples distinguish task retry from exactly-once side effects and cache/persist from reliable checkpointing.
- SVG files parse as XML, have viewBox/title/desc and unique IDs.
- MathML is not nested inside SVG; fractions/scripts have correct child arity; display formulas have accessible scroll regions.
- Interactive algorithm calculators use the stated paper parameters and distinguish theoretical probabilities from empirical accuracy.
- Evidence ledger JSON parses; every claim has a unique ID, non-empty claim/kind/source_url/locator/status/notes, a supported kind/status, and an absolute HTTPS source. Verified claims require a source and locator.
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

- Articles 16–20 include source-located evidence for Parquet / Arrow / Iceberg, DVC, DCLM / Dolma, BPE / SentencePiece and tokenizer-vocabulary trade-offs.
- Storage explanations distinguish Parquet row groups from files, Arrow memory layout from Parquet storage, and object-store consistency from multi-object transactions.
- Reproducibility examples include source, code, config, runtime, tokenizer and output identities; a random seed alone is not treated as a reproducibility guarantee.
- Quality audits report sampling frames, strata, weights and confidence assumptions; no universal scalar quality score is asserted.
- Tokenizer examples label character-BPE as a teaching implementation, not a faithful GPT-2/tiktoken implementation; vocabulary comparisons use matched text and pinned tokenizer revisions.
- Vocabulary calculators distinguish tied vs untied matrices and weight storage from optimizer state, activations and logits buffers.

- Articles 21–25 include source-located evidence for Self-Instruct / Evol-Instruct, DAPT / TAPT / TiC-LM, DataTrove implementation behavior, Dolma Toolkit / Dolma 3 and six cleaning evidence families.
- Synthetic-data examples distinguish generated candidates from validated accepted samples; verifier rates are sequential conditional rates and model-collapse claims are scoped to recursive replacement settings.
- Domain adaptation examples distinguish unlabeled DAPT / TAPT from SFT and measure token exposure after tokenization / packing; no universal replay ratio is asserted.
- DataTrove examples pin CLI/API/defaults to a release tag or commit; v0.10.1 examples must not silently cite moving `main` source. Preserve task count and input shard mapping across retries; task markers are not claimed to provide exactly-once external side effects.
- Dolma pages distinguish dataset snapshot, CLI toolkit release and Dolma 3 recipe repository; Toolkit CLI examples are pinned to v1.2.1, Dolma 3 statistics to a commit, and Bloom-filter hits are not treated as exact duplicate proof.
- Cleaning comparisons separate governance hard gates from quality scoring and report precision / recall alongside retained-distribution shifts.
