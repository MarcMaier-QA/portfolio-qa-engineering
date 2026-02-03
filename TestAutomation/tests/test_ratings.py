import pytest

from TestAutomation.utils.constants import (
    TEST_USER_NAME,
    RATING_REQUIRED_ERROR,
    PRODUCT_CHERRIES,   # Used in TC-03
    PRODUCT_PEARS,
    PRODUCT_ORANGES
)


@pytest.mark.ui
@pytest.mark.rating
def test_5_stars_with_comment(adult_shop, cleanup_review):
    """
    TC-01

    Verifies that a user can submit a 5-star rating with a comment.
    This test intentionally checks a known bug where comments
    may not be displayed correctly after submission.
    """
    product_page = adult_shop.open_product(PRODUCT_ORANGES)

    comment = "Tolles Produkt!"
    number_of_stars = 5

    # Submit rating with stars and comment
    product_page.rate_product(stars=number_of_stars, comment=comment)

    # Wait until the user's review section becomes visible
    product_page.wait_for_user_review(TEST_USER_NAME)

    # Assertion 1: Comment should be visible (known bug may cause failure)
    assert product_page.is_comment_visible(
        TEST_USER_NAME,
        comment
    ), "Comment is missing after submitting a rating."

    # Assertion 2: Displayed star rating should match the submitted value
    assert (
        product_page.get_displayed_rating(TEST_USER_NAME)
        == number_of_stars
    ), "Displayed star rating is incorrect after submitting 5 stars."


@pytest.mark.ui
@pytest.mark.rating
def test_4_stars_without_comment(adult_shop, cleanup_review):
    """
    TC-02

    Verifies that a user can submit a star rating without providing a comment.
    """
    product_page = adult_shop.open_product(PRODUCT_PEARS)

    number_of_stars = 4

    # Submit rating without comment
    product_page.rate_product(stars=number_of_stars)

    # Verify that the correct number of stars is displayed
    assert (
        product_page.get_displayed_rating(TEST_USER_NAME)
        == number_of_stars
    ), "Displayed star rating is incorrect after submitting 4 stars."


@pytest.mark.ui
@pytest.mark.rating
def test_no_stars_with_comment(adult_shop, cleanup_review):
    """
    TC-03

    Negative test:
    Verifies that submitting a comment without selecting any stars
    is rejected and returns the expected validation error message.
    """
    product_page = adult_shop.open_product(PRODUCT_CHERRIES)

    comment = "Gut"
    number_of_stars = 0

    # Submit comment without selecting stars (core of this negative test)
    error_message = product_page.rate_product(
        stars=number_of_stars,
        comment=comment
    )

    # Verify correct validation error message
    assert error_message == RATING_REQUIRED_ERROR, (
        f"Unexpected error message returned: {error_message}"
    )
