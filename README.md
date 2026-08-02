# webshop-tests

BDD test repo for the WebShop application. QE agents, instruction sets, and
governance rules are synced from `qe-agents-central` into `.github/` via PR —
see `.qe-agents.yaml` for what this repo consumes.

- `features/` — Behave features + step definitions (Playwright under the hood)
- `mock-ui/` — static WebShop pages the tests run against
- Run tests:
  ```
  python -m venv .venv
  .venv/Scripts/python -m pip install -r requirements.txt
  .venv/Scripts/python -m playwright install chromium
  behave
  ```
  `behave` and `playwright` live in `.venv` only. `.vscode/settings.json` pins that
  interpreter, so VS Code terminals activate it automatically.

Run `HEADED=1 behave` to watch the browser during a test run.
