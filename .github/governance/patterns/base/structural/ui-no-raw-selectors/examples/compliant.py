"""Compliant examples — no raw selectors in step files.

Two shapes are acceptable, depending on what the repository already has.
"""
from pages.webshop.login_page import LoginPage


# 1. Repo WITH a page-object layer: steps delegate to it.
def step_sign_in(context):
    LoginPage(context.page).sign_in(context.user)


def step_add_to_cart(context, product_builder):
    shop = LoginPage(context.page).sign_in(context.user)
    shop.add_to_cart(product_builder.build())


# 2. Repo WITHOUT a page-object layer: drive the page directly, but locate
#    elements only by test id / role — never a raw CSS or XPath selector.
def step_open_products_page(context):
    context.page.goto(f"{context.base_url}/products.html")


def step_search_for(context, term):
    context.page.get_by_test_id("search-input").fill(term)


def step_count_product_cards(context, count):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == count
