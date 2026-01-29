import pytest

from TestAutomation.utils.constants import (
    PRODUCT_CHERRIES,
    PRODUCT_APPLES,
    SHIPPING_COST_FREE,
    SHIPPING_COST_STANDARD,
    TEN_CHERRIES_SUBTOTAL,
    TWO_CHERRIES_SUBTOTAL,
    SEVEN_CHERRIES_SUBTOTAL,
    PRICE_PINK_LADY_APPLE,
)

@pytest.mark.ui
def test_free_shipping(shop):
    """
    TC-08: Kostenloser Versand bei Erreichen des Schwellenwerts
    """
    shop.add_product_to_cart(PRODUCT_CHERRIES, 10) \
        .go_to_checkout() \
        .verify_shipping_costs(
            expected_shipping=SHIPPING_COST_FREE,
            expected_subtotal=TEN_CHERRIES_SUBTOTAL
        )


def test_standard_shipping(shop):
    """
    TC-09: Kostenpflichtiger Versand unter dem Schwellenwert

    Szenario:
    - Bestellwert: 5.00€ (2x Cherries à 2.50€)
    - Schwellenwert: 20.00€
    - Erwartete Versandkosten: 5.00€ (Standard)

    Prüft ob Versandkosten korrekt berechnet werden wenn
    Bestellwert unter dem Gratis-Schwellenwert liegt.
    """
    cherries_quantity = 2

    shop.add_product_to_cart(PRODUCT_CHERRIES, cherries_quantity)

    checkout = shop.go_to_checkout()
    checkout.verify_shipping_costs(
        expected_shipping=SHIPPING_COST_STANDARD,
        expected_subtotal=TWO_CHERRIES_SUBTOTAL
    )


def test_shipping_update_on_removal(shop):
    """
    TC-10 – KNOWN BUG

    Expected:
    - Shipping cost updates to 5.00€ when cart value drops below threshold

    Actual:
    - Shipping cost remains 0.00€

    This test currently FAILS and documents a business logic bug.
    """
    apple_quantity = 1
    cherries_quantity = 7

    shop.add_product_to_cart(PRODUCT_APPLES, apple_quantity)
    shop.add_product_to_cart(PRODUCT_CHERRIES, cherries_quantity)

    shop.go_to_checkout() \
        .verify_shipping_costs(
        expected_shipping=SHIPPING_COST_FREE,
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL + PRICE_PINK_LADY_APPLE
    ) \
        .remove_product_from_cart(PRODUCT_APPLES) \
        .verify_shipping_costs(
        expected_shipping=SHIPPING_COST_STANDARD,
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL
    )
