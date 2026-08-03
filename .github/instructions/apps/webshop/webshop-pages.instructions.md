---
applyTo: "features/**"
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

## Harness

- `features/environment.py` starts the static server and Playwright; each
  scenario gets a fresh `context.page` already wired to `context.base_url`.
- Run: `behave` from the repo root. `HEADED=1 behave` to watch the browser.
