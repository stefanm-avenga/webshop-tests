"""Violation example - uses raw requests calls in a step file."""
import requests


def step_get_holdings_raw(context, portfolio_id):
    response = requests.get(
        f"{context.api_base}/portfolios/{portfolio_id}/holdings",
        headers={"Authorization": f"Bearer {context.token}"},
    )
    context.last_response = response.json()


def step_create_order_raw(context, order):
    response = requests.post(
        f"{context.api_base}/orders",
        json=order,
        headers={"Authorization": f"Bearer {context.token}"},
    )
    assert response.status_code == 201
