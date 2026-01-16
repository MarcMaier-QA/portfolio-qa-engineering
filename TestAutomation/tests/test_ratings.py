import pytest
from selenium.webdriver.support import expected_conditions as EC

from TestAutomation.pages.product_page import ProductPage
from TestAutomation.utils.constants import (
    PRODUCT_ORANGES_URL,
    PRODUCT_PEARS_URL,
    PRODUCT_CHERRIES_URL,  # Für TC-03
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR  # Für TC-03
)
#todo so wenig navigate wie möglich
#todo: fixture für delete_my_rating
#todo: get_displayed_rating mit wait versehen. z.b jede sekunde versuchen auszuführen für 5 sekunden danach dann abbrechen
#todo: waits in product_page und co ausführen
#todo: tc-01 anpassen das der kommentar geprüft wird wenn gefunden


# optional: logging was ist das und wie setzt man es um
# 1. framework für logging
# 2. conftest mit einbinden
# 3. was sind loglevel wofür braucht man diese
# 4. logeinträge wärend des testens schreiben

# Tests
@pytest.mark.product(PRODUCT_ORANGES_URL)
def test_5_stars_with_comment(clean_reviews):
    """TC-01: 5 Sterne + Kommentar (prüft bekannten Kommentar-Bug)."""
    product = clean_reviews
    comment = "Tolles Produkt!"
    number_of_stars = 5

    (
        product
        .rate_product(stars=number_of_stars, comment=comment)
        .navigate_to(PRODUCT_ORANGES_URL)
    )

    assert product.is_comment_visible(TEST_USER_NAME, comment), "Kommentar fehlt nach Bewertung."
    assert product.get_displayed_rating() == number_of_stars, "Sterne-Anzeige falsch nach 5-Sterne-Bewertung."



@pytest.mark.product(PRODUCT_PEARS_URL)
def test_4_stars_without_comment(clean_reviews):
    """TC-02: 4 Sterne ohne Kommentar."""
    product = clean_reviews
    number_of_stars = 4

    (
        product
        .rate_product(stars=number_of_stars)
        .navigate_to(PRODUCT_PEARS_URL)
    )

    assert product.get_displayed_rating() == number_of_stars, "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."


@pytest.mark.product(PRODUCT_CHERRIES_URL)
def test_no_stars_with_comment(clean_reviews):
    """TC-03: Bewertung ohne Sterne (nur Text). Sollte fehlschlagen und Fehlermeldung anzeigen."""
    product = clean_reviews
    comment = "Gut"
    number_of_stars = 0

    # Kommentar & Sterne (0 Sterne sind der Kern dieses Negativtests)
    error_message = product.rate_product(
        stars=number_of_stars,
        comment=comment
    )

    assert error_message == RATING_REQUIRED_ERROR, f"Falsche Fehlermeldung: {error_message}"
