# Knowledge taxonomy and tag model

## Category vs tag

- Category is one primary learning domain used for the homepage's first-level navigation.
- Tag is an orthogonal concept that can appear in multiple categories.
- Tool names a software package, model or platform.
- Paper is a research anchor; paper names should not be confused with categories.
- Level describes assumed prior knowledge, not scientific importance.

Each chapter has exactly one primary category and may have multiple tags and tools.

## Primary categories

| ID | Label | Scope | Chapters |
|---|---|---|---|
| foundations | 基础与全景 | data lifecycle, provenance, training-corpus framing | 01 |
| acquisition | 数据采集与提取 | Common Crawl, WARC, WAT, WET, HTML extraction | 02–03 |
| cleaning | 规范化与过滤 | language ID, URL/domain, heuristic filters | 04–06 |
| dedup | 去重与相似性 | exact, fuzzy, MinHash, LSH, multi-granularity | 07–09 |
| quality | 质量、安全与评估 | perplexity, educational scoring, labeling, decontamination, evaluation | 10–13, 18 |
| composition | 数据组成与表示 | mixture, tokenization, vocabulary, domain adaptation | 14, 19–20, 22 |
| systems | 系统与工具链 | distributed compute, data lake storage, reproducibility, DataTrove, Dolma | 15–17, 23–24 |
| frontier | 前沿与自动化 | synthetic data, curation paradigms, automation, online selection | 21, 25–27 |
| capstone | 综合实战 | end-to-end project | 28 |

## Tag namespaces

Prefer stable, reusable lowercase tags. Do not create a new spelling for the same concept.

- Process: acquisition, extraction, normalization, language-id, filtering, deduplication, quality-scoring, decontamination, benchmark-contamination, data-mixing, tokenization, reproducibility, llm-annotation, storage, data-lineage.
- Method: heuristics, exact-match, minhash, lsh, jaccard, shingling, bloom-filter, perplexity, cross-entropy, classifier, sampling, ablation, regression, thresholding, rubric, llm-as-judge, inter-annotator-agreement, soft-labels, uncertainty, exact-match, token-level-overlap, suffix-array, token-weighted-sampling, doremi, regmix, dynamic-mixing, partitioning, shuffle, data-skew, checkpointing, backpressure, idempotency, row-group, snapshot, content-hash, stratified-sampling, confidence-interval, wilson-interval, bpe, byte-level-bpe, pre-tokenization, merge-ranks, fertility, bytes-per-token, token-premium, vocabulary-size, parameter-budget.
- Format / data: common-crawl, warc, wat, wet, html, parquet, arrow, jsonl, iceberg, object-storage, data-lake, multilingual, code-data, web-text.
- URL / source governance: url-filtering, url-canonicalization, domain-filtering, blocklist, source-provenance, rfc3986.
- Dedup engineering: sha256, false-positive, paragraph-level, document-level, cross-crawl, dedup-granularity, duplicate-clustering, representative-selection.
- Language-model scoring: ngram, kneser-ney, kenlm, quality-scoring, domain-adaptation.
- Tool: fasttext, trafilatura, warcio, datatrove, dolma, apache-spark, ray-data, pyspark, pyarrow, apache-iceberg, dvc, sentencepiece, tiktoken, huggingface-tokenizers, snowflake-arctic-embed.
- Research anchors: fineweb-edu, doremi, regmix, regmix-d, mt-bench, llama2, gpt3.
- Research anchors: c4, ccnet, the-pile, refinedweb, fineweb, fineweb-edu, dclm, datasheets-for-datasets, dolma, sentencepiece, toklens, byt5, superbpe.
- Concern: privacy, pii, license, bias, label-noise, distribution-shift, train-test-leakage, low-resource-languages, token-premium, data-loss.

## Tag quality rules

1. Use tags to support cross-chapter discovery, not to restate the entire title.
2. Avoid one-off tags unless a named paper, tool or standard is central.
3. Keep names canonical (fasttext, not FastText, fast-text and fastText as separate tags).
4. Add tool tags only when the chapter contains substantive implementation or comparison.
5. Use URL and source-governance tags only when the chapter defines a concrete normalization or filtering policy.
6. Keep method parameters in article text and evidence ledgers; do not encode experimental thresholds as generic tags.
7. Do not infer a paper's conclusion from a tag.
8. Update this taxonomy and courses.json together when introducing a new category or namespace.
