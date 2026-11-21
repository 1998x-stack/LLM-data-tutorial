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
