---
applyTo: '**'
---

# WebShop — Pages & Locators

The mock UI lives in `mock-ui/` and is served by the Behave harness at
`context.base_url` (default `http://localhost:8123`). Locate elements only
via `data-testid` (Playwright `get_by_test_id`) — raw CSS/XPath selectors are
forbidden by governance rule `ui-no-raw-selectors`.

## products.html

| Element | data-testid |
|---|---|
| Page title | `shop-title` |
| Search input | `search-input` |
| Category dropdown | `category-filter` |
| Product card (one per product) | `product-card` |
| Product name (inside card) | `product-name` |
| Product category (inside card) | `product-category` |
| Product price (inside card) | `product-price` |
| Add-to-cart button (inside card) | `add-to-cart` |
| Empty-state message | `no-results` |
| Cart link (header) | `cart-link` |
| Cart item count (header) | `cart-count` |

## cart.html

| Element | data-testid |
|---|---|
| Cart row (one per product) | `cart-item` |
| Item name | `cart-item-name` |
| Item quantity | `cart-item-qty` |
| Item line total | `cart-item-price` |
| Remove button (inside row) | `remove-item` |
| Cart total | `cart-total` |
| Free-shipping banner (≥ $50) | `shipping-banner` |
| Empty-cart message | `empty-cart` |
| Back to products link | `back-link` |

## Repo layout — authoritative for this app

This repo uses a **flat Behave layout with no page-object layer**. Match it exactly:

```
features/                     .feature files live here (flat — no ui/api/db split)
features/steps/               step definitions, one module per feature
features/environment.py       Behave hooks: static server + Playwright lifecycle
mock-ui/                      the application under test — OUT OF SCOPE, never edit
```

- New feature → `features/<name>.feature`; its steps → `features/steps/<name>_steps.py`.
- There are **no page objects, no typed API clients, and no data factories** in this
  repo. Do not create them, and do not import a test-framework base class — none exists.
- Drive Playwright directly from step definitions via `context.page`, using
  `get_by_test_id` with the IDs in the tables above. That is the correct pattern here.
- Follow the style of the existing `features/steps/product_listing_steps.py`.

## Harness

- `features/environment.py` starts the static server and Playwright; each
  scenario gets a fresh `context.page` already wired to `context.base_url`.
- Run: `behave` from the repo root. `HEADED=1 behave` to watch the browser.
- `behave` and `playwright` are installed in `.venv` only; `.vscode/settings.json`
  pins that interpreter so VS Code terminals activate it automatically.
