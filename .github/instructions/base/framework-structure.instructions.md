---
applyTo: '**'
---
# Framework orientation

Before you generate or modify code, orient yourself in the repository you are
actually working in. **Do not assume a layout — read it.**

1. Look at the existing files under the active scope path (see `.qe-projects.yaml`).
2. Follow the conventions already in use there: file naming, directory depth,
   how step definitions locate elements, how test data is built.
3. The app's own instruction overlay (`instructions/apps/<app>/`) is authoritative
   for that app's layout and locator strategy. It overrides anything general here.

## Common layout

Most repositories following this framework use a flat Behave layout:

- `features/` — Gherkin `.feature` files. One scenario per business concern,
  not one per test step.
- `features/steps/` — Python step definitions. Each step is a thin glue layer.
- `features/environment.py` — Behave hooks (`before_all`, `before_scenario`,
  `after_*`). Tag-driven and harness setup belongs here.

Larger suites may add an abstraction layer — page objects, typed API clients,
data factories — and may split `features/` and `steps/` by test type
(`ui`, `api`, `db`). **Where such a layer exists, use it**: keep raw driver and
HTTP calls out of step definitions. Where it does not exist, do not invent one;
write straightforward step definitions in the style already present.

## Rules that hold regardless of layout

- Never introduce a new top-level directory or architectural layer in a PR.
  Adding structure is a platform-team decision, declared in an instruction file.
- If a file you expect is missing, search before assuming — then match what you find.
- Locator and framework specifics come from the app overlay, never from guesswork.
