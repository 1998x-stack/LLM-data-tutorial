# Capstone teaching dataset (invented examples)

All 12 records are fictional sentences written solely to exercise the local
pipeline. They are not scraped, licensed third-party corpus material, or
research measurements. Their license and review flags are **teaching fixtures**
and do not constitute a real rights/privacy audit.

Run:

\`\`\`bash
python3 scripts/capstone_pipeline.py \
  --input examples/capstone/raw.jsonl \
  --policy examples/capstone/policy.json \
  --out /tmp/llm-data-tutorial-capstone
\`\`\`

With the checked-in policy, 5 records are accepted and 7 rejected.
Output is a reproducible release-candidate folder with:

- \`curated.jsonl\`: accepted records with stable source IDs and metadata;
- \`rejected.jsonl\`: reason and ID only, intentionally excluding rejected text;
- \`quality_report.json\`: counts and stated limits;
- \`manifest.json\`: input/policy hashes and output content hashes.

Validate the generated folder:

\`\`\`bash
python3 scripts/capstone_pipeline.py --verify /tmp/llm-data-tutorial-capstone/<run_id>
\`\`\`

The output is **not automatically published**; \`READY_FOR_HUMAN_APPROVAL\`
only means the illustrative deterministic checks passed. No web crawl,
language classifier, PII model, license inference, fuzzy deduplication,
tokenizer, training run or real human review is implemented.
