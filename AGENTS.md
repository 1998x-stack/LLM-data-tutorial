# AGENTS.md — LLM Data Tutorial

This file is the mandatory operating contract for every contributor and coding agent working in this repository.

## Mission

Build an evidence-grounded, graduate-level learning system for LLM pretraining data engineering. The output is an independently useful technical article and a reliable static knowledge base—not a slide deck, marketing page, or a collection of unverified claims.

Use the pedagogical workflow from Olah-style-posts/skills/olah-style-paper-posts/SKILL.md as the reference method:
- progressive explanation: reader misconception → concrete problem → minimal diagram → mechanism → evidence → limitations;
- annotated implementation: explain code in the order the data actually flows;
- original, semantically accurate SVGs;
- executable or inspectable examples;
- static, responsive, accessible HTML.

Do not copy the reference skill's prose, graphics, CSS, logos, or example assets. Apply the method to data engineering topics.

## Repository invariants

1. courses.json is the canonical source for all chapter metadata.
2. courses-data.js is a generated offline projection. Never hand-edit it independently.
3. Keep the public chapter entry points 01.html–28.html stable unless a migration explicitly updates all references.
4. New article content belongs in its numbered chapter file; diagrams belong in assets/diagrams/; factual claim ledgers belong in evidence/.
5. Keep shared presentation in theme.css. Avoid duplicating large inline style blocks.
6. Every article must be understandable without JavaScript. Interactions are progressive enhancement.
7. Production notes, toolchain boasts, “AI-generated” notes and style imitation claims do not belong in article hero, byline or footer.

## Mandatory workflow

### Gate 0 — Inspect before editing
- Read this file, README, relevant chapter, courses.json, adjacent chapters, and existing tests.
- Check current GitHub branch and default branch before writing.
- Preserve existing content outside the requested scope.

### Gate 1 — Research and evidence ledger
- Prefer primary papers, official documentation, standards, and maintained source repositories.
- Read the relevant method, experiment setup, appendix and limitations—not only abstracts.
- For each factual or quantitative claim, record: claim ID, exact statement, source URL, paper version, section/table/figure/line locator, evidence status and notes.
- verified means directly supported; derived means transparently calculated; illustrative means synthetic teaching data; unverified must not be presented as fact.
- Never invent benchmark values, dataset sizes, throughput, percentages, thresholds, author conclusions or API behavior.
- Separate paper results, implementation behavior, engineering recommendations and teaching simplifications.

### Gate 2 — Plan the learning path
For each article write a short map:
reader question → prior misconception → concrete example → diagram question → mechanism → equation / data shape → runnable example → evidence → failure modes.
Each figure must answer one question and have a caption before it is drawn.

### Gate 3 — Author technical content
- Use one H1; ordered H2/H3 hierarchy; semantic main, article, nav, section, figure, figcaption.
- Explain the exact input/output contract and the assumptions of every code example.
- For math, use semantic MathML with accessible descriptions; never fake a substantive formula with Unicode-only text.
- Label toy data and synthetic scores visibly.
- Keep the article's static content complete if JavaScript fails or is disabled.

### Gate 4 — Draw and verify diagrams
- Draw original SVGs; include viewBox, title, desc, accessible name and unique IDs.
- Diagram topology must match the dataflow described in the article.
- Use color consistently within a diagram, but never rely on color alone.
- Keep labels readable on 360px mobile and in print.
- Do not use external images or remote fonts as a substitute for original explanatory figures.

### Gate 5 — Update knowledge architecture
- Add or update category and tag metadata in courses.json.
- Keep tags orthogonal: category = primary knowledge domain; tags = cross-cutting concepts, methods, data formats, papers and tools.
- Update homepage filters and README only when metadata changes require it.
- Preserve offline operation; no mandatory CDN, API or remote runtime dependency.

### Gate 6 — Validate
Run:
    python3 scripts/build_course_data.py --check
    python3 scripts/validate_site.py
    python3 -m unittest discover -s tests -v
    node --test tests/offline-catalog.test.cjs

For visual or interaction changes, run browser QA at 1440×900, 768×1024, 390×844 and 360×800, plus print mode and network-disabled mode. Record screenshots/reports when tooling is available. If browser QA cannot run, report not verified; never call static parsing a browser test.

### Gate 7 — Review and publish
- Inspect every changed path and generated file.
- Review the diff for unsupported claims, dead links, invalid HTML, SVG errors, accessibility regressions, mobile overflow and stale navigation.
- Prefer a focused branch and PR. Check CI status and changed files before merging.
- Verify the default-branch files after merge. GitHub Pages is only live after the deployment workflow and published URL are checked.

## Topic-specific editorial rules

### Data sources
Distinguish a crawl snapshot, archive format, index, raw response, extracted text and final training dataset. Public availability is not completeness or permission to redistribute.

### Extraction and language
Do not treat tag stripping as main-content extraction. Do not treat classifier scores as calibrated probabilities unless calibration is measured. Keep short, mixed-language and low-resource cases visible in evaluation.

### Filtering and deduplication
A threshold is an experimental choice tied to a dataset and target. Report false-positive risk, retained distribution and downstream evaluation. Do not transfer C4/FineWeb settings as universal defaults.

### Quality and data mixing
“High quality” is task-dependent. Report model, dataset, token budget, tokenizer, evaluation protocol and source locator for any model result. Keep document counts distinct from token counts.

### Version-sensitive tools and corpora

- Bind every command, API, default, package requirement and configuration example to an explicit release or commit. Prefer versioned official documentation and source links over unversioned blog posts.
- Distinguish dataset snapshot/version from the toolkit/package version. For example, a Dolma corpus version is not the same thing as a Dolma Toolkit release.
- Label code as verified against the pinned version, illustrative pseudocode, or not executed. Never imply that a snippet was run when it was only transcribed from documentation.
- For benchmark and dataset statistics, record whether the number is full-corpus size, sampled training exposure, tokenized count or a model-specific experimental budget.

## Completion report

A release report must include:
- changed files and purpose;
- primary sources consulted;
- claims corrected or removed;
- tests actually executed and their results;
- browser sizes/interactions verified or explicitly not verified;
- branch, commit, PR and merge status;
- deployment status only if independently checked.


## Algorithmic and mathematical validation

- Derive every probability and complexity formula from a primary paper, standard, or established technical source; record the exact locator in `evidence/NN.json`.
- When a chapter includes a calculator, its UI formula and the dependency-free test helper must implement the same expression. Label theoretical estimates separately from empirical outcomes.
- For URL normalization, preserve original URLs and do not lowercase path/query or strip arbitrary query parameters without a documented equivalence policy.
- For deduplication, distinguish candidate generation, exact verification, clustering, and representative selection. Never describe Bloom Filter `maybe` as exact membership.
- For perplexity, record model, tokenizer, target domain, token-count convention, and language-specific thresholding. Do not interpret lower PPL as universal quality.


### Educational classifiers and LLM-assisted annotation
- Distinguish the target construct (e.g. educational value) from the teacher label and the downstream keep/drop policy.
- Preserve continuous regression scores and thresholded decisions separately; report per-class and slice metrics, not only a single F1.
- LLM-generated labels are noisy measurements. Version the rubric, prompt, model, sampling design and adjudication protocol.
- Select agreement statistics for the measurement scale (nominal, ordinal, continuous); report human-human baselines and uncertainty intervals where appropriate.
- Audit position, verbosity, source-identity and model-family biases. Model ensembles can shift score distributions rather than remove bias.

### Benchmark decontamination
- Separate exact text overlap, syntactic transformation, semantic equivalence, task-level exposure and demonstrated evaluation inflation.
- Reproduce paper-specific tokenization, prompt verbalization, n-gram/skipgram thresholds and common-phrase handling exactly; never present them as universal defaults.
- Store matched spans, offsets, train document IDs, benchmark version and reviewer decisions. A retrieval hit is a candidate, not a verdict.
- Compare clean and contaminated subsets while checking for difficulty and distribution shifts; disclose the audit protocol.

### Data mixtures
- Distinguish document sampling probabilities from token exposure proportions. Record post-tokenization and post-packing token shares.
- State the assumptions behind any document-length conversion; account for truncation, filtering, packing and repeated exposure in production metrics.
- Treat DoReMi, Data Mixing Laws, RegMix and RegMix-D as experimental methods with proxy-to-target transfer assumptions, not universal mixture recipes.
- Report the model scale, tokenizer, token budget, source snapshot and downstream suite for every claimed optimal mix.

### Distributed data processing
- Make the partition key, input manifest, code/config version and output commit protocol explicit.
- Explain where shuffle, global aggregation and hot-key skew occur; profile task duration and memory instead of assuming a universal partition size.
- Distinguish Spark cache/persist, reliable checkpoint and localCheckpoint; distinguish Ray Data blocks, object store, UDF heap and backpressure.
- Task retries may repeat side effects. Use stable idempotency keys, immutable shard outputs and sink-specific commit semantics; do not claim exactly-once without proof.


### Storage and data lake layout
- Distinguish raw archives, normalized columnar datasets, curated table snapshots, training shards and tokenizer-bound token blocks.
- Explain Parquet File → Row Group → Column Chunk → Page accurately. A row group is not a file; row-group sizing is workload-dependent.
- Distinguish Arrow's in-memory columnar representation from Parquet's compressed storage representation.
- Treat Iceberg manifests and snapshots as table-level metadata/commit abstractions; do not equate object-store consistency with multi-object transactions.
- Measure compression, file sizes, scan throughput, metadata cost and small-file compaction on the actual corpus.

### Reproducibility and provenance
- A seed alone is not a reproducibility contract. Include source snapshot, input checksums, code commit, canonical config, environment/dependency lock, model/tokenizer revision, randomness and output checksums.
- Declare whether the requirement is bitwise, semantic or statistical reproducibility.
- Hash canonicalized manifest bytes and sort shard entries before computing dataset digests; validate relative paths, duplicate paths and checksum syntax.
- Distinguish content identity from data correctness, quality, legal provenance and permission to redistribute.

### Corpus quality evaluation
- Do not collapse integrity, coverage, content reliability, redundancy, safety/governance and downstream utility into an opaque universal score.
- Report sampling frame, strata, inclusion probabilities, weights, rubric, inter-annotator process and confidence intervals.
- Compare curation strategies under a fixed model, tokenizer, token budget, training recipe and multi-task evaluation suite.
- Treat DCLM / Dolma results as paper-specific evidence, not universal data-quality guarantees.

### Tokenization and vocabulary
- Distinguish normalizer, pre-tokenizer, byte/character alphabet, merge ranks, special tokens and token-ID mapping.
- Character-BPE teaching code is not a drop-in GPT-2/tiktoken implementation; label all omitted stages.
- Pin tokenizer revisions when reporting token counts. Compare parallel texts using corpus token count (CTC) / reference-normalized token premium; bytes-per-token alone is not a fair cross-language compression metric because byte premiums differ.
- Vocabulary costs include embedding and possibly untied LM-head weights, logits width and token-frequency allocation; report tied/untied assumptions and excluded memory terms.
- Do not infer language complexity from token fertility or claim a single vocabulary size is universally optimal.


## Batch 06 final-three production discipline
- Chapters 26–28 complete the learning graph; maintain 01–28 status and category/tags/prerequisites in courses.json, then regenerate courses-data.js. Update homepage completion count, README and evidence ledgers together.
- For automated preparation (26), draw explicit boundaries between untrusted source content, planner, sandbox runner, deterministic checks and privileged release controller. Stop on rights/privacy hard gates and require independent approval.
- For dynamic mixing (27), DoReMi learns proxy-stage weights via excess loss and Group DRO; RegMix selects fixed mixtures by regression; RegMix-D has offline and online variants; ODM and AC-ODM update online. Do not mislabel any as another algorithm or claim universal gain.
- For capstone (28), keep the stdlib example executable, deterministic and versioned. Distinguish source metadata flags from independently verified legal/privacy clearance; make rejected output omit raw text, compute output checksums, validate idempotent reruns and tampering, and never auto-publish.
- Full-repository review must inspect existing 01–25 as well as the new 26–28, not merely the changed files. Report CI, branch/PR status, Pages and browser QA separately; archive a findings-and-fixes review record.
