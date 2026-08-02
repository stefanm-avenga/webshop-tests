---
applyTo: '**'
---
# UI step definitions — Playwright

When you generate or modify UI step definitions:

**Respect the repo's abstraction layer**
- If the repository has page object classes, step definitions delegate to them.
  A step body should be one to three lines of page-object calls.
- If it does not, drive Playwright directly from the step definition using the
  page handle the Behave harness provides on `context` — but keep steps thin and
  readable. Do not introduce a page-object layer that the repo does not already have.

**Selector discipline (applies either way)**
- Prefer `data-testid` (`get_by_test_id`). If unavailable, prefer accessible role
  queries (`get_by_role`) over CSS or XPath.
- Raw CSS/XPath selector calls are blocked by the `ui-no-raw-selectors` governance
  rule, which fails the PR.
- Where page objects exist, selectors are constants on the class, not inline
  strings in method bodies.
- Hard-coded waits (`sleep`, `wait_for_timeout`) are not permitted. Use `expect()`
  assertions or `wait_for_*` with explicit conditions.

**Browser state and parallelism**
- Each scenario gets a fresh browser context via Behave hooks in `environment.py`.
  Do not assume cookies, storage, or session state carry between scenarios.
- Steps must be idempotent within a scenario — re-running it from scratch must
  produce the same result.

**Cross-domain scenarios**
- Hybrid `@ui @api` scenarios share state via Behave's `context` object only —
  never via module-level globals.
