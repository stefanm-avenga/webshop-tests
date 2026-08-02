---
applyTo: "**/*.py"
---
# Framework orientation

This test repository follows a standardized layout. Before you generate or modify code, orient yourself by the folder:

- `features/{ui,api,db}/` — Gherkin `.feature` files. One scenario per business concern, not one per test step.
- `steps/{ui,api,db}/` — Python step definitions. Each step is a thin glue layer; logic lives in page objects, clients, or domain helpers.
- `pages/<app>/` — Page Object classes. Extend `BasePage` from PyAutocore. Encapsulate every Playwright call here; expose semantic methods (`sign_in`, `submit_order`), not raw locators.
- `clients/<app>/` — API client classes. Extend `BaseClient` from PyAutocore. Return typed dataclasses, never raw `requests.Response` objects.
- `utils/data_factory.py` — Test data builders. Use the builder pattern with sensible defaults; return dataclasses.
- `environment.py` — Behave hooks (`before_all`, `before_feature`, `before_scenario`, `after_*`). Tag-driven setup belongs here.
- `performance/` — Locust performance scenarios. Compose PyAutocore personas and load shapes; do not duplicate test logic from `steps/`.

When a file you need to reference is not in this orientation, search the codebase before assuming it doesn't exist — but never invent a layer outside this list without an instruction file declaring it. Adding folders is a platform-team decision, not an in-PR decision.
