import re
import pytest
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.pages.checkout_page import CheckoutPage
from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.utils.constants import (
    PRODUCT_CHERRIES,
    PRODUCT_APPLES,
    SHIPPING_COST_FREE,  # 0.00 €
    SHIPPING_COST_STANDARD,  # 5.00 €
    TEN_CHERRIES_SUBTOTAL,  # 25.00 €
    TWO_CHERRIES_SUBTOTAL,  # 5.00 €
    SEVEN_CHERRIES_SUBTOTAL,  # 17.50 €
    PRICE_PINK_LADY_APPLE  # 2.50 €
)


def clean_currency(currency_string: str) -> float:
    """Extrahiert den Preis als Float aus einem String wie '95.00€'"""
    cleaned_string = re.sub(r'€', '', currency_string)
    cleaned_string = cleaned_string.replace(',', '.').strip()
    return float(cleaned_string)


# Basis-Fixture für Setup
@pytest.fixture
def setup_cart_environment(login):
    """Führt allgemeines Setup aus (Login, Popup, leeren des Warenkorbs)."""
    driver = login
    shop_page = ShopPage(driver)
    checkout_page = CheckoutPage(driver)
    age_popup = AgeVerificationPopup(driver)

    checkout_page.clear_cart_if_not_empty()
    shop_page.navigate_to_shop()
    age_popup.confirm_age()

    return driver, shop_page, checkout_page


def run_shipping_assertions(checkout_page, expected_shipping_cost, expected_subtotal):
    """Zentrale Funktion zur Ausführung der Konvertierung und Assertions."""

    # 1. Preise auslesen
    product_total_actual_str = checkout_page.get_product_total()
    shipping_cost_actual_str = checkout_page.get_shipping_cost()
    total_actual_str = checkout_page.get_total()

    # 2. Konvertierung zu float
    product_total_actual = clean_currency(product_total_actual_str)
    shipping_cost_actual = clean_currency(shipping_cost_actual_str)
    total_actual = clean_currency(total_actual_str)

    # 3. Erwartete Gesamtsumme berechnen
    total_expected = product_total_actual + expected_shipping_cost

    # Sicherstellen, dass die Zwischensumme (Produktkosten) korrekt ist
    assert product_total_actual == expected_subtotal, \
        f"Zwischensumme inkorrekt. Erwartet: {expected_subtotal:.2f}€, Tatsächlich: {product_total_actual:.2f}€"

    # 4. A) Prüfe Versandkosten
    assert shipping_cost_actual == expected_shipping_cost, \
        (f"Versandkosten inkorrekt (TC-Check). Erwartet: {expected_shipping_cost:.2f}€, "
         f"Tatsächlich: {shipping_cost_actual:.2f}€")

    # 5. B) Prüft Gesamtsumme (Produktkosten + Versandkosten)
    assert total_actual == total_expected, \
        (f"Gesamtsumme inkorrekt. Erwartet: {total_expected:.2f}€, "
         f"Tatsächlich: {total_actual:.2f}€")

    return checkout_page  # Gibt das Objekt für weitere Schritte zurück


# TC-08: Kostenlos ab 25 €
def test_tc08_free_shipping_at_threshold(setup_cart_environment):
    """TC-08: Bestellwert (25 €) erreicht Schwellenwert (20 €) -> Erwartet 0.00 € Versand."""
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge Produkt hinzu (10x Cherries = 25.00 €)
    shop_page.add_product_to_cart(product_name=PRODUCT_CHERRIES, quantity=10)

    # 2. Zum Checkout navigieren
    checkout_page.navigate_to_checkout()

    # 3. Assertions durchführen
    run_shipping_assertions(
        checkout_page,
        expected_shipping_cost=SHIPPING_COST_FREE,  # ERWARTET: 0.00 €
        expected_subtotal=TEN_CHERRIES_SUBTOTAL  # 25.00 €
    )


# TC-09: Kostenpflichtig unter 25 €
def test_tc09_standard_shipping_below_threshold(setup_cart_environment):
    """TC-09: Bestellwert (5 €) unter Schwellenwert (20 €) -> Erwartet 5.00 € Versand."""
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge Produkt hinzu (2x Cherries = 5.00 €)
    shop_page.add_product_to_cart(product_name=PRODUCT_CHERRIES, quantity=2)

    # 2. Zum Checkout navigieren
    checkout_page.navigate_to_checkout()

    # 3. Assertions durchführen
    run_shipping_assertions(
        checkout_page,
        expected_shipping_cost=SHIPPING_COST_STANDARD,  # ERWARTET: 5.00 €
        expected_subtotal=TWO_CHERRIES_SUBTOTAL  # 5.00 €
    )


# TC-10: BUG TEST (Dynamisches Update)
@pytest.mark.xfail(reason="BUG: Versandkosten werden nach Produktentfernung nicht neu berechnet (bleiben 0.00 €).")
def test_tc10_shipping_update_on_removal(setup_cart_environment):
    """TC-10: Prüft das Bug-Szenario: Versandkosten bleiben 0.00 € nach Reduzierung unter den Schwellenwert."""
    driver, shop_page, checkout_page = setup_cart_environment

    # 1. Füge genug Produkte für kostenlosen Versand hinzu (7x Cherries + 1x Apples = 20.00 €)
    shop_page.add_product_to_cart(product_name=PRODUCT_CHERRIES, quantity=7)
    shop_page.add_product_to_cart(product_name=PRODUCT_APPLES, quantity=1)  # Annahme: Preis 2.50 €

    # 2. Zum Checkout navigieren
    checkout_page.navigate_to_checkout()

    # 3. Initialprüfung (Bestätigt 0.00 € Versand)
    run_shipping_assertions(
        checkout_page,
        expected_shipping_cost=SHIPPING_COST_FREE,  # 0.00 €
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL + PRICE_PINK_LADY_APPLE  # 20.00 €
    )

    # 4. Produkt entfernen (Warenwert fällt auf 17.50 €)
    # 💥 HIER wird eine Methode in deiner CheckoutPage benötigt, um das Produkt zu entfernen.
    checkout_page.remove_product_from_cart(product_name=PRODUCT_APPLES)

    # 5. Erneute Assertion: ERWARTET 5.00 € Versandkosten (BUG-Check)
    run_shipping_assertions(
        checkout_page,
        expected_shipping_cost=SHIPPING_COST_STANDARD,  # ERWARTET: 5.00 €
        expected_subtotal=SEVEN_CHERRIES_SUBTOTAL  # 17.50 €
    )
