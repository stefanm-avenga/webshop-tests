"""Compliant example — uses page object, no raw selectors in step files."""
from pages.webshop.login_page import LoginPage


def step_sign_in(context):
    LoginPage(context.page).sign_in(context.user)


def step_add_to_cart(context, product_builder):
    shop = LoginPage(context.page).sign_in(context.user)
    shop.add_to_cart(product_builder.build())
