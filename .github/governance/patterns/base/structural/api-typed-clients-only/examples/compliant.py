"""Compliant example - uses typed PyAutocore client, no raw requests in step files."""
from clients.webshop.product_client import ProductClient
from clients.webshop.cart_client import CartClient


def step_list_products(context, category):
    products = ProductClient(context.client).list_by_category(category)
    context.last_response = products


def step_add_to_cart(context, cart_builder):
    cart_item = cart_builder.build()
    response = CartClient(context.client).add_item(cart_item)
    context.last_response = response
