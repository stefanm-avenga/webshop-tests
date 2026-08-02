"""Step definitions for the product listing feature."""

from behave import given, then


@given("the shop products page is open")
def step_open_products_page(context):
    context.page.goto(f"{context.base_url}/products.html")


@then("{count:d} product cards are displayed")
def step_count_product_cards(context, count):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == count, f"expected {count} cards, got {cards.count()}"


@then("every product card shows a name and a price")
def step_cards_show_name_and_price(context):
    cards = context.page.get_by_test_id("product-card")
    for i in range(cards.count()):
        card = cards.nth(i)
        assert card.get_by_test_id("product-name").inner_text().strip()
        assert card.get_by_test_id("product-price").inner_text().startswith("$")
