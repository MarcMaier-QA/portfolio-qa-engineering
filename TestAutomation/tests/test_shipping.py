import re
import pytest
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.pages.checkout_page import CheckoutPage
from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.utils.constants import PRODUCT_APPLES, PRODUCT_CHERRIES

def clean_currency(currency_string: str) -> float:
    """"Extrahiert den Preis als Float aus einem String wie '95.00€'"""
    # Entfernt das '€'
    cleaned_string = re.sub(r'[€]', '', currency_string)
    return float(cleaned_string)

def test_shipping_costs_calculation(login):
    """TC-08: Prüft die korrekte Berechnung der Versandkosten und die Gesamtsumme."""
    driver = login

    # 1. Instanziierung der Seitenobjekte
    shop_page = ShopPage(driver)
    checkout_page = CheckoutPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # 2. Altersabfrage bestätigen
    age_popup.confirm_age()

    # 3. Warenkorb leeren (Sauberer start)
    checkout_page.clear_cart_if_not_empty()

    # 4. Produkt zum Wahrenkorb hinzufügen
    shop_page.navigate_to_shop()

    # 5. Füge Produkt 1 hinzu (z.b Kirschen)
    shop_page.add_product_to_cart(product_name=PRODUCT_CHERRIES, quantity=10)

    # 6. Zum Checkout navigieren
    checkout_page.navigate_to_checkout()

    # 7. Preis auslesen und konvertieren
    product_total_actual_str = checkout_page.get_product_total()
    shipping_cost_actual_str = checkout_page.get_shipping_cost()
    total_actual_str = checkout_page.get_total()

    # 8. Kovertierung zu float
    product_total_actual = clean_currency(product_total_actual_str)
    shipping_cost_actual = clean_currency(shipping_cost_actual_str)
    total_actual = clean_currency(total_actual_str)

    # 9. Erwartete Werte definieren (Annahme basierend auf Projekt-Spezifikation)
    SHIPPING_COST_EXPECTED = 25.00

    # 10. Assertions durchführen
    # A) Prüfe Versandkosten
    assert shipping_cost_actual == SHIPPING_COST_EXPECTED, \
        f"Versandkosten inkorrekt. Erwartet: {SHIPPING_COST_EXPECTED:.2f}€, Tatsächlich: {shipping_cost_actual:.2f}€"

    # B) Prüft Gesamtsumme (Produktkosten + Versandkosten)
    total_expected = product_total_actual + SHIPPING_COST_EXPECTED
    assert total_actual == total_expected, \
        f"Gesamtsumme inkorrekt. Erwartet: {total_expected:.2f}€, Tatsächlich: {total_actual:.2f}€"