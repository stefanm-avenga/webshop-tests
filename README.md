# webshop-tests

BDD test repo for the WebShop application. QE agents, instruction sets, and
governance rules are synced from `qe-agents-central` into `.github/` via PR —
see `.qe-agents.yaml` for what this repo consumes.

- `features/` — Behave features + step definitions (Playwright under the hood)
- `mock-ui/` — static WebShop pages the tests run against
- Run tests: `pip install -r requirements.txt && playwright install chromium && behave`
