---
applyTo: "steps/ui/**/*.py"
---
# UI step definitions — Playwright + page object pattern

When you generate or modify UI step definitions (`steps/ui/**/*.py`):

**Call page objects, never raw Playwright**
- Step definitions delegate to methods on page object classes in `pages/<app>/`. A step body should be one to three lines of page-object calls, possibly with a builder-pattern setup from `utils/data_factory.py`.
- Raw selector calls (`page.locator(...)`, `page.get_by_role(...)`, etc.) are not permitted in step files. The `ui-no-raw-selectors` Semgrep rule (loaded automatically when you edit a `steps/ui/**/*.py` file) blocks merge on violations.

**Selectors live in page objects only**
- Inside `pages/`, prefer `data-testid` attributes. If `data-testid` is unavailable, prefer accessible role queries (`get_by_role`) over CSS or XPath.
- Hard-coded waits (`sleep`, `wait_for_timeout`) are not permitted. Use `expect()` assertions or `wait_for_*` with explicit conditions.
- Selectors are constants on the page object class, not inline strings inside method bodies.

**Browser state and parallelism**
- Each scenario gets a fresh browser context via Behave hooks in `environment.py`. Do not assume cookies, storage, or session state carry between scenarios.
- Steps must be idempotent within a scenario — re-running the scenario from scratch must produce the same result.

**Cross-domain scenarios**
- Hybrid `@ui @api` scenarios split their step implementations across `steps/ui/` and `steps/api/`. They share state via Behave's `context` object only — never via module-level globals.
