"""Step definitions for the product search feature."""

from behave import then, when
from playwright.sync_api import expect


@when('the user searches for "{term}"')
def step_search_for(context, term):
    context.page.get_by_test_id("search-input").fill(term)


@when('the user selects the "{category}" category')
def step_select_category(context, category):
    context.page.get_by_test_id("category-filter").select_option(category)


@when("the user clears the search")
def step_clear_search(context):
    context.page.get_by_test_id("search-input").fill("")


@then("no product cards are displayed")
def step_no_product_cards(context):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == 0, f"expected 0 cards, got {cards.count()}"


@then('the product named "{name}" is shown')
def step_product_named_shown(context, name):
    names = context.page.get_by_test_id("product-name")
    found = any(names.nth(i).inner_text().strip() == name for i in range(names.count()))
    assert found, f'product "{name}" not found in visible cards'


@then("the no-results message is shown")
def step_no_results_shown(context):
    expect(context.page.get_by_test_id("no-results")).to_be_visible()
