import time

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
    PRICE_PINK_LADY_APPLE
)


@pytest.fixture
def setup_cart_environment(login):
    """
    Basis-Fixture für Versandkosten-Tests.

    Führt allgemeines Setup aus:
    - Login (via login fixture)
    - Leeren des Warenkorbs
    - Navigation zum Shop
    - Bestätigung der Altersverifikation

    Returns:
        Tuple: (driver, shop_page, checkout_page)
    """
    driver = login
    shop_page = ShopPage(driver)
    checkout_page = CheckoutPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # Warenkorb leeren (falls noch Produkte drin sind)
    checkout_page.clear_cart_if_not_empty()

    # Zum Shop navigieren
    shop_page.navigate_to_shop()

    # Altersverifikation bestätigen
    age_popup.confirm_age()

    return driver, shop_page, checkout_page


def verify_shipping_costs(checkout_page: CheckoutPage,expected_shipping: float,expected_subtotal: float):
    """
    Zentrale Hilfsfunktion für Versandkosten-Assertions.

    Prüft:
    1. Zwischensumme (Produktkosten) ist korrekt
    2. Versandkosten sind korrekt
    3. Gesamtsumme (Produkte + Versand) ist korrekt

    Args:
        checkout_page: CheckoutPage Instanz
        expected_shipping: Erwartete Versandkosten
        expected_subtotal: Erwartete Produkt-Zwischensumme
    """
    # 1. Preise als Float auslesen
    actual_subtotal = checkout_page.get_product_total_as_float()
    actual_shipping = checkout_page.get_shipping_cost_as_float()
    actual_total = checkout_page.get_total_as_float()

    # 2. Erwartete Gesamtsumme berechnen
    expected_total = expected_subtotal + expected_shipping

    # 3. Assertion: Zwischensumme (Produktkosten)
    assert actual_subtotal == expected_subtotal, (
        f"Produkt-Zwischensumme inkorrekt. "
        f"Erwartet: {expected_subtotal:.2f}€, "
        f"Tatsächlich: {actual_subtotal:.2f}€"
    )

    # 4. Assertion: Versandkosten
    assert actual_shipping == expected_shipping, (
        f"Versandkosten inkorrekt. "
        f"Erwartet: {expected_shipping:.2f}€, "
        f"Tatsächlich: {actual_shipping:.2f}€"
    )

    # 5. Assertion: Gesamtsumme
    assert actual_total == expected_total, (
        f"Gesamtsumme inkorrekt. "
        f"Erwartet: {expected_total:.2f}€ (Produkte: {expected_subtotal:.2f}€ + Versand: {expected_shipping:.2f}€), "
        f"Tatsächlich: {actual_total:.2f}€"
    )


def test_tc08_free_shipping_at_threshold(setup_cart_environment):
    """
    TC-08: Kostenloser Versand bei Erreichen des Schwellenwerts

    Szenario:
    - Bestellwert: 25.00€ (10x Cherries à 2.50€)
    - Schwellenwert: 20.00€
    - Erwartete Versandkosten: 0.00€ (gratis)

    Prüft ob der kostenlose Versand korrekt angewendet wird.
    """
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge Produkte hinzu (10x Cherries = 25.00€)
    time.sleep(0.3)
    shop_page.add_product_to_cart(
        product_name=PRODUCT_CHERRIES,
        quantity=10
    )

    # 2. Navigiere zum Checkout
    checkout_page.navigate_to_checkout()

    # 3. Verifiziere alle Preise
    verify_shipping_costs(
        checkout_page,
        expected_shipping=SHIPPING_COST_FREE,  # 0.00€
        expected_subtotal=TEN_CHERRIES_SUBTOTAL  # 25.00€
    )


def test_tc09_standard_shipping_below_threshold(setup_cart_environment):
    """
    TC-09: Kostenpflichtiger Versand unter dem Schwellenwert

    Szenario:
    - Bestellwert: 5.00€ (2x Cherries à 2.50€)
    - Schwellenwert: 20.00€
    - Erwartete Versandkosten: 5.00€ (Standard)

    Prüft ob Versandkosten korrekt berechnet werden wenn
    Bestellwert unter dem Gratis-Schwellenwert liegt.
    """
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge Produkte hinzu (2x Cherries = 5.00€)
    shop_page.add_product_to_cart(
        product_name=PRODUCT_CHERRIES,
        quantity=2
    )

    # 2. Navigiere zum Checkout
    checkout_page.navigate_to_checkout()

    # 3. Verifiziere alle Preise
    verify_shipping_costs(
        checkout_page,
        expected_shipping=SHIPPING_COST_STANDARD,  # 5.00€
        expected_subtotal=TWO_CHERRIES_SUBTOTAL  # 5.00€
    )


@pytest.mark.xfail(
    reason="BUG: Versandkosten werden nach Produktentfernung nicht aktualisiert. "
           "Bleiben bei 0.00€ obwohl Warenwert unter Schwellenwert fällt."
)
def test_tc10_shipping_update_on_removal(setup_cart_environment):
    """
    TC-10: Dynamisches Update der Versandkosten (BUG-Test)

    Szenario:
    1. Warenwert über Schwellenwert -> 0.00€ Versand
    2. Produkt entfernen -> Warenwert fällt unter Schwellenwert
    3. Versandkosten sollten auf 5.00€ aktualisiert werden

    Bekannter Bug:
    Versandkosten bleiben bei 0.00€ nach Entfernen von Produkten,
    auch wenn der Warenwert unter den Schwellenwert fällt.
    """
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge genug Produkte für kostenlosen Versand hinzu
    #    7x Cherries (17.50€) + 1x Apples (2.50€) = 20.00€
    time.sleep(0.3)

    shop_page.add_product_to_cart(
        product_name=PRODUCT_APPLES,
        quantity=1
    )

    time.sleep(0.3)

    shop_page.add_product_to_cart(
        product_name=PRODUCT_CHERRIES,
        quantity=7
    )

    # 2. Navigiere zum Checkout
    checkout_page.navigate_to_checkout()

    # 3. Initiale Prüfung: Versandkosten sollten 0.00€ sein
    verify_shipping_costs(
        checkout_page,
        expected_shipping=SHIPPING_COST_FREE,  # 0.00€
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL + PRICE_PINK_LADY_APPLE  # 20.00€
    )

    # 4. Entferne ein Produkt (Warenwert fällt auf 17.50€)
    checkout_page.remove_product_from_cart(product_name=PRODUCT_APPLES)

    # 5. BUG-Check: Versandkosten sollten jetzt 5.00€ sein
    #    (tatsächlich bleiben sie bei 0.00€)
    verify_shipping_costs(
        checkout_page,
        expected_shipping=SHIPPING_COST_STANDARD,  # ERWARTET: 5.00€
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL  # 17.50€
    )