import pytest
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.pages.checkout_page import CheckoutPage
from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.utils.constants import (
    PRODUCT_CHERRIES,
    PRODUCT_APPLES,
    SHIPPING_COST_FREE,
    SHIPPING_COST_STANDARD,
    TEN_CHERRIES_SUBTOTAL,
    TWO_CHERRIES_SUBTOTAL,
    SEVEN_CHERRIES_SUBTOTAL,
    PRICE_PINK_LADY_APPLE,
    PRODUCT_CHERRIES_URL
)


@pytest.fixture
def clean_cart(login):
    driver = login
    checkout = CheckoutPage(driver)

    checkout.clear_cart_if_not_empty()

    yield driver

    checkout.clear_cart_if_not_empty()


@pytest.fixture
def shop(clean_cart):
    driver = clean_cart
    shop = ShopPage(driver)
    age = AgeVerificationPopup(driver)
    shop.navigate_to_shop()
    age.confirm_age()
    return shop


@pytest.mark.product(PRODUCT_CHERRIES_URL)
def test_free_shipping(shop):
    """
    TC-08: Kostenloser Versand bei Erreichen des Schwellenwerts

    Szenario:
    - Bestellwert: 25.00€ (10x Cherries à 2.50€)
    - Schwellenwert: 20.00€
    - Erwartete Versandkosten: 0.00€ (gratis)

    Prüft ob der kostenlose Versand korrekt angewendet wird.
    """
    cherries_quantity = 10

    shop.add_product_to_cart(PRODUCT_CHERRIES, cherries_quantity)

    (
        CheckoutPage(shop.driver)
        .goto_checkout()
        .verify_shipping_costs(
            expected_shipping=SHIPPING_COST_FREE,
            expected_subtotal=TEN_CHERRIES_SUBTOTAL
        )
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

    (
        CheckoutPage(shop.driver)
        .goto_checkout()
        .verify_shipping_costs(
            expected_shipping=SHIPPING_COST_STANDARD,
            expected_subtotal=TWO_CHERRIES_SUBTOTAL
        )
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

    (
        CheckoutPage(shop.driver)
        .goto_checkout()
        .verify_shipping_costs(
            expected_shipping=SHIPPING_COST_FREE,
            expected_subtotal=SEVEN_CHERRIES_SUBTOTAL + PRICE_PINK_LADY_APPLE
        )
        .remove_product_from_cart(PRODUCT_APPLES)
        .verify_shipping_costs(
            expected_shipping=SHIPPING_COST_STANDARD,
            expected_subtotal=SEVEN_CHERRIES_SUBTOTAL
        )
    )

