# Quality gates and release checklist

## Static gates

- courses.json parses and contains unique chapter numbers and valid category IDs.
- courses-data.js is reproducibly generated from courses.json.
- Every chapter file exists and every local chapter link resolves.
- Articles 01–25 have one H1, semantic main/article/nav, figure captions, accessible MathML where formulas are used, primary references and a structured evidence/NN.json ledger.
- Algorithm examples have dependency-free unit tests for URL semantics, Bloom parameters, Jaccard, LSH candidate probability, perplexity score conversion, document-to-token mixture math, storage capacity estimates, manifest fingerprints, Wilson intervals, BPE merges and vocabulary parameter costs.
- Articles 11–15 distinguish synthetic teaching values from empirical paper results and include source locators for verified quantitative claims.
- Annotation exercises state that LLM labels are noisy measurements; contamination detection separates overlap from task leakage; data-mixture examples distinguish document shares from token shares.
- Distributed-processing examples distinguish task retry from exactly-once side effects and cache/persist from reliable checkpointing.
- SVG files parse as XML, have viewBox/title/desc and unique IDs.
- MathML is not nested inside SVG; fractions/scripts have correct child arity; display formulas have accessible scroll regions.
- Interactive algorithm calculators use the stated paper parameters and distinguish theoretical probabilities from empirical accuracy.
- Evidence ledger JSON parses; every claim has a unique ID, supported kind/status, HTTPS source, locator and explanatory notes; verified claims must be directly supported.
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
- Articles 21–25 bind synthetic-data claims to Self-Instruct, Evol-Instruct, Phi-4 and model-collapse sources; domain-adaptation claims to DAPT/TAPT research; DataTrove examples to v0.10.1; Dolma Toolkit examples to v1.2.1; and corpus versions/licenses to the current dataset card.
- Chapter 25 compares C4, CCNet, The Pile, RefinedWeb, FineWeb, Dolma and FLUX by method and scope; cross-paper benchmark numbers must not be combined unless model, tokenizer, token budget, data snapshot and evaluation protocol are comparable.
- Storage explanations distinguish Parquet row groups from files, Arrow memory layout from Parquet storage, and object-store consistency from multi-object transactions.
- Reproducibility examples include source, code, config, runtime, tokenizer and output identities; a random seed alone is not treated as a reproducibility guarantee.
- Quality audits report sampling frames, strata, weights and confidence assumptions; no universal scalar quality score is asserted.
- Tokenizer examples label character-BPE as a teaching implementation, not a faithful GPT-2/tiktoken implementation; vocabulary comparisons use matched text and pinned tokenizer revisions.
- Vocabulary calculators distinguish tied vs untied matrices and weight storage from optimizer state, activations and logits buffers.
