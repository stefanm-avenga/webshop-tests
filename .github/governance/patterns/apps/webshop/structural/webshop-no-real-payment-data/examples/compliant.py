def test_checkout_with_saved_card(card_factory):
    card = card_factory.build(token="4242-TEST")  # obviously-fake placeholder
    submit_payment(card.token)
