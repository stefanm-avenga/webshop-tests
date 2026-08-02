"""Order-service endpoint stubs for the WebShop backend.

Application internals: not part of the BDD test suite.
"""
from dataclasses import dataclass, field


@dataclass
class OrderItem:
    product_id: int
    quantity: int


@dataclass
class CreateOrderRequest:
    customer_id: int
    items: list = field(default_factory=list)


class OrdersService:
    """In-memory stand-in for the real order service."""

    def __init__(self) -> None:
        self._orders = {}
        self._next_id = 1

    def create_order(self, request: CreateOrderRequest) -> int:
        if not request.items:
            raise ValueError("an order needs at least one item")
        order_id = self._next_id
        self._orders[order_id] = request
        self._next_id += 1
        return order_id

    def get_order(self, order_id: int) -> CreateOrderRequest:
        return self._orders[order_id]

    def cancel_order(self, order_id: int) -> None:
        self._orders.pop(order_id, None)
