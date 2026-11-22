# Evidence, citations and claim provenance

## Evidence ledger

Every deeply revised chapter has evidence/NN.json. Each entry includes:
- id: stable claim ID;
- claim: concise factual statement;
- kind: paper-result, paper-method, official-doc, implementation, standard, derived, or illustrative;
- source_url: canonical source;
- locator: section, table, figure, official documentation heading or source version;
- status: verified, derived, illustrative, or unverified;
- notes: scope, assumptions, caveats and version.

## Claim classes

- Paper method: what the authors say they did.
- Paper result: a result under the paper's exact model, data, token budget and evaluation protocol.
- Official documentation: supported API behavior or dataset format.
- Implementation behavior: behavior verified in a named tool/version.
- Standard: normative requirements or definitions from a formal specification such as an RFC or published standard.
- Derived: a transparent calculation from cited values.
- Illustrative: invented toy inputs for teaching, clearly labeled as synthetic.

Never turn an illustrative value into an empirical statistic. Never present a paper result as a universal engineering guarantee.

## Metrics checklist

For every numeric result record:
- model and parameter count;
- dataset and version;
- tokenizer and token budget;
- benchmark, split, metric and direction;
- baseline and controlled comparison;
- paper section/table/figure;
- seed count or uncertainty when reported.

If any field is missing, omit the number or explicitly qualify the missing context.

## Citation placement

- Link the primary paper at first substantial mention.
- Cite the exact section/table/figure nearest the claim.
- For software-specific claims, link official docs or source code and name the version if relevant.
- For CLI/API/default/configuration behavior, use a release-tagged or commit-pinned source URL. A moving `main` URL is not an immutable evidence locator; if living docs are unavoidable, record the access date and do not use them as the sole source for version-specific behavior.
- Avoid citation chains where a blog summarizes a paper that is available directly.
- Publicly downloadable data may still have license, privacy and redistribution restrictions.
