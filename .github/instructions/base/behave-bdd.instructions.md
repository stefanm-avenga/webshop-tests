---
applyTo: "features/**/*.feature"
---
# Gherkin authoring — Behave conventions

When you write `.feature` files in this repository:

**Scenario shape**
- One scenario describes one observable business behavior. If a scenario needs more than ~7 `Given/When/Then` steps to express, it is probably two scenarios.
- `Given` establishes preconditions, `When` performs the single action under test, `Then` asserts the observable result. `And`/`But` chain within a clause but do not change its meaning.
- Use `Scenario Outline` with `Examples` only when the variation is genuinely data-driven (same flow, different inputs). Do not use outlines to compress logically distinct scenarios.

**Step phrasing**
- Phrase steps from the user's perspective, not the implementation's. Prefer "When the user submits the order" over "When the order POST is called."
- Reuse existing step phrases verbatim when the meaning matches — the step registry is shared across features. Search `steps/` before authoring a new phrase.
- Step phrases use plain English; do not embed selectors, URLs, or other implementation detail in the Gherkin.

**Tags**
- Tag scenarios with `@ui`, `@api`, or `@db` to indicate which step folder is the primary owner. Hybrid scenarios are tagged with both (e.g. `@ui @api`).
- Tag with the JIRA ticket key (`@SHOP-1234`) so failures trace back. The Zephyr Draft→Active promotion uses this tag.
- Do not invent new tags without a corresponding hook in `environment.py`.
