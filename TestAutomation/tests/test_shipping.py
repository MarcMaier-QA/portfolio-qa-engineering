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
def test_free_shipping(adult_shop):
    """
    TC-08: Free shipping when the threshold is reached.
    """
    cherries_quantity = 10

    adult_shop.add_product_to_cart(PRODUCT_CHERRIES, quantity=cherries_quantity)

    checkout = adult_shop.go_to_checkout()
    checkout.wait_until_totals_updated(TEN_CHERRIES_SUBTOTAL)

    totals = checkout.get_totals()

    assert totals["subtotal"] == TEN_CHERRIES_SUBTOTAL, (
        f"Expected subtotal {TEN_CHERRIES_SUBTOTAL}, "
        f"but got {totals['subtotal']}"
    )
    assert totals["shipping"] == SHIPPING_COST_FREE, (
        f"Expected shipping {SHIPPING_COST_FREE}, "
        f"but got {totals['shipping']}"
    )
    assert totals["total"] == TEN_CHERRIES_SUBTOTAL + SHIPPING_COST_FREE,(
        f"Expected total {TEN_CHERRIES_SUBTOTAL + SHIPPING_COST_FREE}, "
        f"but got {totals['total']}"
    )


def test_standard_shipping(adult_shop):
    """
    TC-09: Paid shipping below the threshold

    Szenario:
    - Order value: 5.00€ (2x Cherries à 2.50€)
    - Threshold: 20.00€
    - Expected shipping costs: 5.00€ (Standard)

    Checks if shipping costs are calculated correctly when the
    order value is below the free shipping threshold.
    """
    cherries_quantity = 2

    adult_shop.add_product_to_cart(PRODUCT_CHERRIES, cherries_quantity)

    checkout = adult_shop.go_to_checkout()
    checkout.wait_until_totals_updated(TWO_CHERRIES_SUBTOTAL)

    totals = checkout.get_totals()

    assert totals["subtotal"] == TWO_CHERRIES_SUBTOTAL, (
        f"Expected subtotal {TWO_CHERRIES_SUBTOTAL}, "
        f"but got {totals['subtotal']}"
    )
    assert totals["shipping"] == SHIPPING_COST_STANDARD, (
        f"Expected shipping {SHIPPING_COST_STANDARD}, "
        f"but got {totals['shipping']}"
    )
    assert totals["total"] == TWO_CHERRIES_SUBTOTAL + SHIPPING_COST_STANDARD, (
        f"Expected total {TWO_CHERRIES_SUBTOTAL + SHIPPING_COST_STANDARD}, "
        f"but got {totals['total']}"
    )


def test_shipping_update_on_removal(adult_shop):
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

    adult_shop.add_product_to_cart(PRODUCT_APPLES, apple_quantity)
    adult_shop.add_product_to_cart(PRODUCT_CHERRIES, cherries_quantity)

    checkout = adult_shop.go_to_checkout()
    checkout.wait_until_totals_updated(
        SEVEN_CHERRIES_SUBTOTAL + PRICE_PINK_LADY_APPLE
    )

    totals = checkout.get_totals()
    assert totals["shipping"] == SHIPPING_COST_FREE, (
        f"Expected shipping {SHIPPING_COST_FREE}, "
        f"but got {totals['shipping']}"
    )

    checkout.remove_product_from_cart(PRODUCT_APPLES)
    checkout.wait_until_totals_updated(SEVEN_CHERRIES_SUBTOTAL)

    totals = checkout.get_totals()

    # FAILS – documented business logic bug
    assert totals["shipping"] == SHIPPING_COST_STANDARD, (
        f"Expected shipping {SHIPPING_COST_STANDARD}, "
        f"but got {totals['shipping']}"
    )

