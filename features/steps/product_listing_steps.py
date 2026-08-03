"""Step definitions for the product listing feature."""

from behave import given, then, when


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


@when('the user searches for "{text}"')
def step_search_for(context, text):
    context.page.get_by_test_id("search-input").fill(text)


@when('the user selects the "{category}" category')
def step_select_category(context, category):
    context.page.get_by_test_id("category-filter").select_option(category)


@when("the user clears the search")
def step_clear_search(context):
    context.page.get_by_test_id("search-input").fill("")


@then('only products containing "{text}" in their name are shown')
def step_only_products_with_name(context, text):
    cards = context.page.get_by_test_id("product-card")
    count = cards.count()
    assert count > 0, f"expected at least one product card matching '{text}'"
    for i in range(count):
        name = cards.nth(i).get_by_test_id("product-name").inner_text()
        assert text.lower() in name.lower(), f"product '{name}' does not contain '{text}'"


@then('only products in the "{category}" category containing "{text}" in their name are shown')
def step_only_products_in_category_with_name(context, category, text):
    cards = context.page.get_by_test_id("product-card")
    count = cards.count()
    assert count > 0, f"expected at least one product card in '{category}' matching '{text}'"
    for i in range(count):
        card = cards.nth(i)
        name = card.get_by_test_id("product-name").inner_text()
        cat = card.get_by_test_id("product-category").inner_text()
        assert text.lower() in name.lower(), f"product '{name}' does not contain '{text}'"
        assert cat == category, f"product category '{cat}' is not '{category}'"


@then("no product cards are displayed")
def step_no_product_cards(context):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == 0, f"expected 0 cards, got {cards.count()}"


@then('the message "{message}" is shown')
def step_message_is_shown(context, message):
    no_results = context.page.get_by_test_id("no-results")
    assert no_results.is_visible(), "no-results message element is not visible"
    actual = no_results.inner_text().strip()
    assert actual == message, f"expected '{message}', got '{actual}'"
