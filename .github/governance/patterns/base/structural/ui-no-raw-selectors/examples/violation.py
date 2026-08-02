"""Violation example — uses raw page.locator() in a step file."""


def step_sign_in_with_raw_selectors(context):
    page = context.page
    page.locator('[data-testid="email"]').fill(context.user.email)
    page.locator('[data-testid="password"]').fill(context.user.password)
    page.locator('[data-testid="submit"]').click()
