"""Step definitions for the product search feature."""

from behave import then, when
from playwright.sync_api import expect


@when('the user searches for "{term}"')
def step_search_for_term(context, term):
    context.page.get_by_test_id("search-input").fill(term)


@when('the user filters by the "{category}" category')
def step_filter_by_category(context, category):
    context.page.get_by_test_id("category-filter").select_option(category)


@when("the user clears the search")
def step_clear_search(context):
    context.page.get_by_test_id("search-input").fill("")


@then('the product named "{name}" is shown')
def step_product_named_is_shown(context, name):
    names = context.page.get_by_test_id("product-name")
    found = any(
        names.nth(i).inner_text().strip() == name for i in range(names.count())
    )
    assert found, f'Product "{name}" not found in the grid'


@then('the "{message}" message is shown')
def step_message_is_shown(context, message):
    no_results = context.page.get_by_test_id("no-results")
    expect(no_results).to_be_visible()
    assert no_results.inner_text().strip() == message


# Singular form for "1 product card is displayed"
@then("{count:d} product card is displayed")
def step_count_product_cards_singular(context, count):
    cards = context.page.get_by_test_id("product-card")
    assert cards.count() == count, f"expected {count} cards, got {cards.count()}"
