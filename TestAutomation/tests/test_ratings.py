from TestAutomation.utils.constants import (
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR,
    PRODUCT_CHERRIES,  # Für TC-03
    PRODUCT_PEARS,
    PRODUCT_ORANGES
)


def test_5_stars_with_comment(adult_shop, cleanup_review):
    """TC-01: 5 Sterne + Kommentar (prüft bekannten Kommentar-Bug)."""
    product_page = adult_shop.open_product(PRODUCT_ORANGES)

    comment = "Tolles Produkt!"
    number_of_stars = 5

    product_page.rate_product(stars=number_of_stars, comment=comment)

    # Warten bis Review - Bereich für User sichtbar ist
    product_page.wait_for_user_review(TEST_USER_NAME)

    # Assert 1: Bewertung existiert
    assert product_page.is_comment_visible(TEST_USER_NAME, comment), "Kommentar fehlt nach Bewertung."

    # Assert 2: Sterne sind korrekt
    assert (
            product_page.get_displayed_rating(TEST_USER_NAME)
            == number_of_stars), "Sterne-Anzeige falsch nach 5-Sterne-Bewertung."



def test_4_stars_without_comment(adult_shop, cleanup_review):
    """TC-02: 4 Sterne ohne Kommentar."""
    product_page = adult_shop.open_product(PRODUCT_PEARS)

    number_of_stars = 4

    product_page.rate_product(stars=number_of_stars)

    assert (
            product_page.get_displayed_rating(TEST_USER_NAME)
            == number_of_stars), "Sterne-Anzeige falsch nach 4-Sterne-Bewertung."


def test_no_stars_with_comment(adult_shop, cleanup_review):
    """TC-03: Bewertung ohne Sterne (nur Text). Sollte fehlschlagen und Fehlermeldung anzeigen."""
    product_page = adult_shop.open_product(PRODUCT_CHERRIES)

    comment = "Gut"
    number_of_stars = 0

    # Kommentar & Sterne (0 Sterne sind der Kern dieses Negativtests)
    error_message = product_page.rate_product(
        stars=number_of_stars,
        comment=comment
    )

    assert error_message == RATING_REQUIRED_ERROR, f"Falsche Fehlermeldung: {error_message}"
