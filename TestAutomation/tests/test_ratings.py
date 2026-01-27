from TestAutomation.utils.constants import (
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR  # Für TC-03
)

# optional: logging was ist das und wie setzt man es um
# 1. framework für logging
# 2. conftest mit einbinden
# 3. was sind loglevel wofür braucht man diese
# 4. logeinträge wärend des testens schreiben

def test_5_stars_with_comment(oranges_product_page):
    """TC-01: 5 Sterne + Kommentar (prüft bekannten Kommentar-Bug)."""
    oranges_product_page.delete_my_review()

    comment = "Tolles Produkt!"
    number_of_stars = 5

    oranges_product_page.rate_product(stars=number_of_stars, comment=comment)

    # Warten bis Review - Bereich für User sichtbar ist
    oranges_product_page.wait_for_user_review(TEST_USER_NAME)

    assert oranges_product_page.is_comment_visible(TEST_USER_NAME, comment), "Kommentar fehlt nach Bewertung."
    assert (
            oranges_product_page.get_displayed_rating(TEST_USER_NAME)
            == number_of_stars), "Sterne-Anzeige falsch nach 5-Sterne-Bewertung."


def test_4_stars_without_comment(pears_product_page):
    """TC-02: 4 Sterne ohne Kommentar."""
    number_of_stars = 4

    pears_product_page.rate_product(stars=number_of_stars)

    assert (pears_product_page.get_displayed_rating(TEST_USER_NAME)
            == number_of_stars), "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."


def test_no_stars_with_comment(cherries_product_page):
    """TC-03: Bewertung ohne Sterne (nur Text). Sollte fehlschlagen und Fehlermeldung anzeigen."""
    comment = "Gut"
    number_of_stars = 0

    # Kommentar & Sterne (0 Sterne sind der Kern dieses Negativtests)
    error_message = cherries_product_page.rate_product(
        stars=number_of_stars,
        comment=comment
    )

    assert error_message == RATING_REQUIRED_ERROR, f"Falsche Fehlermeldung: {error_message}"
