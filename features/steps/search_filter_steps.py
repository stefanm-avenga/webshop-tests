"""Step definitions for the product search filter feature."""

from behave import when, then


@when('the user searches for "{term}"')
def step_search_for(context, term):
    context.page.get_by_test_id("search-input").fill(term)


@when('the user filters by category "{category}"')
def step_filter_by_category(context, category):
    context.page.get_by_test_id("category-filter").select_option(category)


@when("the user clears the search")
def step_clear_search(context):
    context.page.get_by_test_id("search-input").fill("")


@then('only products whose name contains "{term}" are displayed')
def step_only_matching_products(context, term):
    cards = context.page.get_by_test_id("product-card")
    count = cards.count()
    assert count > 0, f"expected at least one card matching '{term}', got 0"
    for i in range(count):
        name = cards.nth(i).get_by_test_id("product-name").inner_text().strip()
        assert term.lower() in name.lower(), (
            f"card '{name}' does not contain '{term}'"
        )


@then("no product cards are displayed")
def step_no_product_cards(context):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == 0, f"expected 0 cards, got {cards.count()}"


@then('the "{message}" message is shown')
def step_message_is_shown(context, message):
    locator = context.page.get_by_test_id("no-results")
    assert locator.is_visible(), "expected no-results message to be visible"
    assert locator.inner_text().strip() == message, (
        f"expected '{message}', got '{locator.inner_text().strip()}'"
    )
