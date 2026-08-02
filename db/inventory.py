"""Inventory repository for the WebShop backend.

Application internals: not part of the BDD test suite.
"""
import sqlite3


class InventoryRepository:
    def __init__(self, db_path: str = "webshop.db") -> None:
        self._conn = sqlite3.connect(db_path)

    def on_hand(self, product_id: int) -> int:
        row = self._conn.execute(
            "SELECT on_hand FROM inventory WHERE product_id = ?", (product_id,)
        ).fetchone()
        return row[0] if row else 0

    def needs_reorder(self) -> list:
        rows = self._conn.execute(
            "SELECT product_id FROM inventory WHERE on_hand <= reorder_at"
        ).fetchall()
        return [r[0] for r in rows]

    def adjust(self, product_id: int, delta: int) -> None:
        self._conn.execute(
            "UPDATE inventory SET on_hand = on_hand + ? WHERE product_id = ?",
            (delta, product_id),
        )
        self._conn.commit()
