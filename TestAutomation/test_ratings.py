import pytest
from pages.product_page import ProductPage

from Hausübungen.Selenium_grundlage_aufgabe1_login_script import product
from Hausübungen.tests.conftest import driver
from TestAutomation.utils.constants import PRODUCT_ORANGES_URL, PRODUCT_PEARS_URL, TEST_USER_NAME
from selenium.common.exceptions import TimeoutException

# Tests
def test_5_stars_with_comment(login):
    """TC-01: 5 Sterne mit Kommentar (Prüft den bekannten Kommentar-Bug)."""
    driver = login
    product_page = ProductPage(driver)

    # 1. Navigation
    product_page.navigate_to(PRODUCT_ORANGES_URL)

    # 2. Kommentar & Sterne
    comment = "Tolles Produkt!"
    try:
        # Versucht, das Produkt zu bewerten
        product_page.rate_product(stars=5, comment=comment)
    except TimeoutException:
        # Tritt ein, wenn das Produkt nicht bewertbar ist z.b noch nicht gekauft
        pytest.skip("Bewertungsformular nicht sichtbar. Produkt vermutlich nicht gekauft.")

    # 3. Assertion: Testet den BUG
    # Die Methode is_comment_visible übernimmt die komplette Logik von verify_comment.
    assert product_page.is_comment_visible(author=TEST_USER_NAME, comment_text=comment) == False,\
        "Der Kommentar wurde unerwartet angezeigt. TC-01 ist unerwartet PASSED."


def test_4_stars_without_comment(login):
    """TC-02: 4 Sterne ohne Kommentar"""
    driver = login
    product_page = ProductPage(driver)

    # 1. Navigation
    product_page.navigate_to(PRODUCT_PEARS_URL)

    # 2. Aktion: Nur Sterne setzen
    try:
        product_page.rate_product(stars=4)
    except TimeoutException:
        # Tritt ein, wenn das Produkt nicht bewertbar ist z.b noch nicht gekauft
        pytest.skip("Bewertungsformular nicht sichtbar. Produkt vermutlich nicht gekauft.")

    assert product_page.get_displayed_rating() == 4, "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."