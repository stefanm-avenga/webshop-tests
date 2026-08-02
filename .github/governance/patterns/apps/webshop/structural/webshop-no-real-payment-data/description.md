# webshop-no-real-payment-data

Test code and fixtures must never contain strings formatted like payment card
numbers (16 digits, optionally dash/space separated). Even fake-but-plausible
numbers normalise pasting real data into tests and trip DLP scanners.

**Instead:** use obviously-invalid placeholders ("4242-TEST") or generate
payment fixtures through a data factory.

- Severity: error (structural — Semgrep-enforced at PR time)
- Scope: `features/**/*.py` in the webshop consumer repo
