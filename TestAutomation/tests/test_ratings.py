import pytest
from TestAutomation.pages.product_page import ProductPage
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.utils.constants import (
    PRODUCT_ORANGES_URL,
    PRODUCT_PEARS_URL,
    PRODUCT_CHERRIES_URL,  # Für TC-03
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR  # Für TC-03
)
# todo: funktion zum löschen der kommentare/bewertung
# todo: page objekt chaining

# Tests
def test_5_stars_with_comment(login):
    """TC-01: 5 Sterne + Kommentar (prüft bekannten Kommentar-Bug)."""
    driver = login
    product_page = ProductPage(driver)
    comment = "Tolles Produkt!"
    number_of_stars = 5

    # 1. Navigation
    product_page.navigate_to(PRODUCT_ORANGES_URL)

    # Formular muss sichtbar sein für eine bewertung
    assert product_page.can_rate_product(), "Bewertungsformular fehlt."

    # 2. Kommentar & Sterne
    product_page.rate_product(stars=number_of_stars, comment=comment)

    # 3. Reload für die sichtbarkeit
    product_page.navigate_to(PRODUCT_ORANGES_URL)

    assert product_page.is_comment_visible(TEST_USER_NAME, comment), "Kommentar fehlt nach Bewertung."
    assert product_page.get_displayed_rating() == number_of_stars, "Sterne-Anzeige falsch nach 5-Sterne-Bewertung."

    # Bewertung löschen
    product_page.delete_my_review()


def test_4_stars_without_comment(login):
    """TC-02: 4 Sterne ohne Kommentar."""
    driver = login
    product_page = ProductPage(driver)
    number_of_stars = 4

    # 1. Navigation
    product_page.navigate_to(PRODUCT_PEARS_URL)

    if not product_page.can_rate_product():
        pytest.skip("Bewertungsformular nicht sichtbar – Produkt nicht gekauft.")

    # 2. Aktion: Nur Sterne setzen
    product_page.rate_product(stars=number_of_stars)

    product_page.navigate_to(PRODUCT_PEARS_URL)

    # 3. Warte, bis die UI mit "(4)" aktualisiert wurde
    product_page.wait.until(
        EC.text_to_be_present_in_element(product_page.DISPLAYED_RATING, "4") #
    )
    assert product_page.get_displayed_rating() == 4, "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."

    # Bewertung löschen
    product_page.delete_my_review()


def test_no_stars_with_comment(login):
    """TC-03: Bewertung ohne Sterne (nur Text). Sollte fehlschlagen und Fehlermeldung anzeigen."""
    driver = login
    product_page = ProductPage(driver)
    comment = "Gut"
    number_of_stars = 0

    # 1. Navigation
    product_page.navigate_to(PRODUCT_CHERRIES_URL)

    if not product_page.can_rate_product():
        pytest.skip("Bewertungsformular nicht sichtbar – Produkt nicht gekauft.")

    # 2. Kommentar & Sterne (0 Sterne sind der Kern dieses Negativtests)
    error_message = product_page.rate_product(
        stars=number_of_stars,
        comment=comment
    )

    assert error_message == RATING_REQUIRED_ERROR