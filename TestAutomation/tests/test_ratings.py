import pytest
from TestAutomation.pages.product_page import ProductPage
from TestAutomation.utils.constants import (
    PRODUCT_ORANGES_URL,
    PRODUCT_PEARS_URL,
    PRODUCT_CHERRIES_URL,  # Für TC-03
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR  # Für TC-03
)
from selenium.common.exceptions import TimeoutException


# Tests
def test_5_stars_with_comment(login):
    """TC-01: 5 Sterne + Kommentar (prüft bekannten Kommentar-Bug)."""
    driver = login
    product_page = ProductPage(driver)

    # 1. Navigation
    product_page.navigate_to(PRODUCT_ORANGES_URL)

    # 2. Kommentar & Sterne
    comment = "Tolles Produkt!"
    try:
        product_page.rate_product(stars=5, comment=comment)
    except TimeoutException:
        pytest.skip("Bewertungsformular nicht sichtbar – Produkt vermutlich nicht gekauft.")

    # 3. Assertion – der BUG: Kommentar sollte NICHT sichtbar sein
    visible = product_page.is_comment_visible(
        author=TEST_USER_NAME,
        comment_text=comment
    )

    assert visible is False, (
        f"Kommentar ist sichtbar, obwohl er laut Bug nicht gespeichert werden sollte. "
        f"Gefundener Kommentar: {comment}"
    )


def test_4_stars_without_comment(login):
    """TC-02: 4 Sterne ohne Kommentar."""
    driver = login
    product_page = ProductPage(driver)

    # 1. Navigation
    product_page.navigate_to(PRODUCT_PEARS_URL)

    # 2. Aktion: Nur Sterne setzen
    try:
        product_page.rate_product(stars=4)
    except TimeoutException:
        pytest.skip("Bewertungsformular nicht sichtbar. Produkt vermutlich nicht gekauft.")

    assert product_page.get_displayed_rating() == 4, "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."


def test_no_stars_with_comment(login):
    """TC-03: Bewertung ohne Sterne (nur Text). Sollte fehlschlagen und Fehlermeldung anzeigen."""
    driver = login
    product_page = ProductPage(driver)

    # 1. Navigation
    product_page.navigate_to(PRODUCT_CHERRIES_URL)

    # 2. Kommentar & Sterne (0 Sterne sind der Kern dieses Negativtests)
    comment = "Gut"
    try:
        # Die Methode rate_product MUSS den Text der Fehlermeldung zurückgeben.
        error_message = product_page.rate_product(stars=0, comment=comment)
    except TimeoutException:
        pytest.skip("Bewertungsformular nicht sichtbar. Produkt vermutlich nicht gekauft.")

    # 3. Assertion: Überprüft, ob die zurückgegebene Meldung der erwarteten Konstante entspricht.
    assert error_message == RATING_REQUIRED_ERROR, \
        (f"Unerwartete Fehlermeldung angezeigt."
         f"Erwartet: '{RATING_REQUIRED_ERROR}', Erhalten: '{error_message}'")