---
applyTo: "features/**"
---

# WebShop — Domain Knowledge

WebShop is a small e-commerce storefront: a product catalogue with search and
category filtering, and a shopping cart.

## Catalogue

- 8 products across 3 categories: Electronics, Home, Stationery.
- Every product has a name, a category, and a price in USD.

## Search & filtering rules

- Search matches on product **name**, case-insensitive, substring match.
- Search and category filter **combine** (AND semantics).
- When no product matches, the grid is empty and a "No products match your
  search." message is shown.
- Clearing the search restores the full (or category-filtered) list.

## Cart rules

- Adding the same product again increments its quantity (no duplicate rows).
- Cart total = sum of price × quantity.
- Orders of **$50.00 or more qualify for free shipping** — the cart page shows
  a free-shipping banner at or above that threshold.
- Removing the last item shows the empty-cart message.
- The cart persists across page reloads (browser localStorage).

## Test data conventions

- Reference catalogue products by exact name (e.g. "Wireless Mouse").
- Never put real-looking payment data in fixtures — governance rule
  `webshop-no-real-payment-data` enforces this at PR time.
