# Article authoring standard

This guide adapts the workflow in Olah-style-posts/skills/olah-style-paper-posts/SKILL.md to LLM data engineering.

## Required narrative arc

1. Question / misconception: begin with a concrete engineering question.
2. Baseline: show the naive method and why it fails.
3. Mental model: introduce one simple diagram before detailed mechanisms.
4. Mechanism: explain each stage, field, transformation and edge.
5. Equation or data contract: define variables, units, shapes, normalization and assumptions.
6. Implementation: provide a minimal code path that can be inspected or run.
7. Evidence: connect paper claims to section/table/figure and experiment scope.
8. Failure modes: show false positives, false negatives, bias, scale limits and version differences.
9. Synthesis: summarize what the reader can now decide or implement.

## Figure contract

- Each figure answers one question and has a factual caption.
- Use 2–5 progressive states for complex mechanisms rather than one overloaded diagram.
- SVG must include xmlns, viewBox, title, desc, unique IDs and an accessible name.
- Label arrows and data artifacts; distinguish control flow from data flow.
- Use color as a secondary encoding, never the only encoding.
- Minimum practical label size should remain readable at 360px viewport and in print.
- Keep standalone SVGs in assets/diagrams/ and link them from semantic figure elements.

## Math and code

- Substantive formulas use semantic MathML with accessible descriptions.
- Display equations sit inside keyboard-focusable horizontal scroll regions.
- Do not place MathML inside SVG.
- Code examples must state dependencies, input assumptions, output contract and omitted production concerns.
- Mark toy data and synthetic scores as illustrative.
- Never call a snippet production-ready unless retries, validation, observability, resource limits and failure behavior are addressed.

## Interactivity

- Each control answers one named question.
- Use native buttons, inputs and labels with visible focus and aria-live output.
- Provide a meaningful static default state before JavaScript executes.
- No autoplay, remote runtime dependency, analytics or unexplained canvas.
- A control must change a meaningful output, not just decoration.

## Page semantics

- One H1, ordered H2/H3 hierarchy, main, article, nav, section, figure, figcaption.
- Skip link and keyboard-visible focus.
- Sources cited close to claims and listed at the end.
- Avoid a fixed sidebar that covers the reading area on mobile.
- Keep production notes out of article prose.


## Batch 03 topic-specific authoring checks

- Educational scoring: state the construct being measured, the teacher-label protocol, the student model architecture, the hold-out population and the downstream threshold policy separately.
- LLM annotation: version the rubric, prompt and judge model; require schema validation and evidence spans; select agreement statistics for the label scale; audit position, verbosity and source-identity bias.
- Benchmark decontamination: distinguish exact, syntactic, semantic and task-level contamination; record tokenizer, verbalized prompt, match spans and corpus versions; never treat a candidate match as proof of answer leakage.
- Data mixture: derive document sampling weights separately from token exposure; include mean-length assumptions and validate actual post-tokenization/post-packing proportions.
- Distributed processing: identify map vs shuffle boundaries, hot-key skew, memory pools and checkpoint semantics; make retried shard outputs idempotent.
- MathML: use semantic MathML for formulas unless a documented local renderer is part of the page. Do not leave raw TeX delimiters such as \\( ... \\) in a page that has no TeX renderer.
- Interactive examples: label synthetic data as synthetic, keep static explanations complete, and unit-test the same mathematical expression used by the calculator.


## Batch 04 topic-specific authoring checks

- Storage: explain File → Row Group → Column Chunk → Page; distinguish persistent Parquet, in-memory Arrow and table-level Iceberg snapshots. Do not equate object-store strong consistency with a multi-object transaction.
- Reproducibility: identify source snapshot, input checksums, code commit, canonical config, environment lock, model/tokenizer revision, randomness and output manifest. State whether the target is bitwise, semantic or statistical reproduction.
- Quality evaluation: separate integrity, coverage, redundancy, governance and downstream utility. Define the sample frame, strata, weights, rubric, uncertainty and fixed training recipe.
- BPE: distinguish pre-tokenization from merge training, character symbols from UTF-8 bytes, and BPE from Unigram. Label simplified code as a teaching implementation.
- Vocabulary: calculate embedding and optional untied output-head costs explicitly; state what memory terms are excluded. Compare languages with parallel texts using CTC / reference-normalized token premium and pinned tokenizer revisions; bytes-per-token alone is confounded by byte premium.
- MathML: use explicit multiplication operators in matrix-size formulas and keep raw TeX delimiters out of pages without a TeX renderer.


## Batch 05 topic-specific authoring checks

- Synthetic data: separate seed design, generation, independent verification, deduplication, safety / privacy review and downstream utility. Record teacher model, revision, prompt, decoding config, provenance and verifier versions. Do not claim a universal synthetic-data share or imply all synthetic data causes model collapse.
- Domain adaptation: distinguish DAPT, TAPT, continual pretraining and SFT. Report token exposure after filtering, tokenization and packing. Evaluate domain gains and general retention on time- and domain-stratified held-out sets; avoid universal replay ratios.
- DataTrove: describe Document, PipelineStep, task, worker, rank and executor using the pinned version. Keep task count and input mapping stable across retries; document optional extras and external side effects.
- Dolma: distinguish original dataset, Dolma Toolkit CLI and Dolma 3 dataset recipes. Explain attributes sidecars, Bloom false positives, mixer semantics, token output index and version-specific licenses.
- Cleaning paradigms: define the six evidence families and their distinct error/cost profiles. Keep license, privacy, safety and benchmark decontamination as governance gates. Report confusion-matrix metrics and downstream ablations.


## Batch 06 topic-specific authoring checks

- Automation: distinguish planner proposals, sandbox execution, deterministic asset checks, independent release control and human authorization. No unverified "DataEvolver" project or invented industry speedups. Treat raw crawl content as untrusted data, not agent instructions.
- Dynamic mixing: separate fixed mixture, offline curriculum, proxy-derived offline selection, proxy-trajectory scheduling and target-time online feedback. DoReMi Group DRO is not simple high-loss sampling; RegMix-D has offline and online variants.
- Feedback-demo formula: temperature softmax plus uniform exploration floor is a teaching approximation, not a reproduction of DoReMi / ODM / AC-ODM. Keep same normalization in Python and JS tests; use fixed signal semantics and preserve provenance of actual token exposure.
- Capstone: code must run locally without external data/model downloads; include fixture and policy, exact output and rejection counts, hash manifest, tamper detection, idempotency and tests. Do not claim source flags replace real rights or privacy review.
- Review: independently verify CI, source-ledger consistency, article nav, tags, links, SVG XML, MathML, all JS controls, empty/invalid input behavior, main branch and Pages. Record unrun browser screenshots as not verified.
