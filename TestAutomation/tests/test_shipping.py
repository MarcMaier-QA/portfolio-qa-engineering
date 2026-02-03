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
@pytest.mark.shipping
def test_free_shipping(adult_shop):
    """
    TC-08

    Verifies that free shipping is applied once the free-shipping
    threshold is reached.
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
    assert totals["total"] == TEN_CHERRIES_SUBTOTAL + SHIPPING_COST_FREE, (
        f"Expected total {TEN_CHERRIES_SUBTOTAL + SHIPPING_COST_FREE}, "
        f"but got {totals['total']}"
    )


@pytest.mark.ui
@pytest.mark.shipping
def test_standard_shipping(adult_shop):
    """
    TC-09

    Verifies that standard shipping costs are applied when the
    order value is below the free-shipping threshold.

    Scenario:
    - Order value: 5.00€ (2x Cherries at 2.50€)
    - Free-shipping threshold: 20.00€
    - Expected shipping costs: 5.00€
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


@pytest.mark.ui
@pytest.mark.shipping
@pytest.mark.known_bug
def test_shipping_update_on_removal(adult_shop):
    """
    TC-10 – KNOWN BUG

    Verifies that shipping costs are recalculated when the cart
    value drops below the free-shipping threshold after removing
    a product.

    Expected behavior:
    - Shipping cost updates from 0.00€ to 5.00€

    Actual behavior:
    - Shipping cost incorrectly remains at 0.00€

    This test is expected to FAIL and documents a business logic bug.
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

    # Fails due to documented business logic bug
    assert totals["shipping"] == SHIPPING_COST_STANDARD, (
        f"Expected shipping {SHIPPING_COST_STANDARD}, "
        f"but got {totals['shipping']}"
    )
