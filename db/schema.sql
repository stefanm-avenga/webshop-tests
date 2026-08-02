-- WebShop relational schema (reference copy for the data team).
-- Application internals: not part of the BDD test suite.

CREATE TABLE products (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    category     TEXT NOT NULL,
    price_cents  INTEGER NOT NULL CHECK (price_cents >= 0),
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE orders (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL,
    status       TEXT NOT NULL DEFAULT 'pending',
    placed_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE order_items (
    order_id     INTEGER NOT NULL REFERENCES orders(id),
    product_id   INTEGER NOT NULL REFERENCES products(id),
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE inventory (
    product_id   INTEGER PRIMARY KEY REFERENCES products(id),
    on_hand      INTEGER NOT NULL DEFAULT 0,
    reorder_at   INTEGER NOT NULL DEFAULT 5
);
