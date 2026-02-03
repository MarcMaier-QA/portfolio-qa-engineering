import pytest
from TestAutomation.pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_allows_access_to_alcohol(login):
    """
    COMPLIANCE TEST: TC-04

    Verifies that adult users are allowed to access alcoholic products
    after successfully passing the age verification.
    """
    user_is_over_eighteen = "27-08-2007"

    # Navigate from home page to shop
    home = HomePage(login)
    shop = home.go_to_shop()

    # Age verification popup must appear
    popup = shop.age_popup
    assert popup.is_popup_displayed(), "The age verification popup did not appear."

    # Submit a valid birthdate
    popup.submit_birthdate(user_is_over_eighteen)
    assert popup.is_success_message_displayed(), (
        "'You are of age' confirmation message should be visible."
    )

    # Try to access the alcohol category
    shop.filter_alcohol()
    shop.wait_until_shop_ready()

    # Adult users should see alcoholic products
    assert shop.has_visible_products(), (
        "Alcohol products should be visible for users who are 18 or older."
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_blocks_underage_user(login):
    """
    COMPLIANCE TEST: TC-05

    Verifies that underage users are blocked from accessing
    alcoholic products after age verification.
    """
    user_is_under_eighteen = "27-08-2015"

    # Navigate to shop
    home = HomePage(login)
    shop = home.go_to_shop()

    # Age verification popup must appear
    popup = shop.age_popup
    assert popup.is_popup_displayed(), "Age verification popup should be visible."

    # Submit an underage birthdate
    popup.submit_birthdate(user_is_under_eighteen)
    assert popup.is_warning_message_displayed(), (
        "Warning message should be displayed for underage users."
    )

    # Attempt to access alcohol category
    shop.filter_alcohol()

    # Underage notice should be shown
    assert shop.is_underage_notice_visible(), (
        "Underage notice should be visible in the alcohol category."
    )

    # Safety check: no alcohol products should be visible
    assert not shop.has_visible_products(), (
        "Alcohol products must not be visible for underage users."
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_without_birthdate_shows_error(login):
    """
    COMPLIANCE TEST: TC-06

    Verifies that confirming the age verification without entering
    a birthdate classifies the user as underage.
    """
    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup

    # Confirm without entering a birthdate
    popup.click_confirm()

    # A warning message should be displayed
    assert popup.is_warning_message_displayed(), (
        "A warning message should appear when no birthdate is entered."
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_invalid_date_format(login):
    """
    COMPLIANCE TEST: TC-07

    Verifies that invalid date formats are rejected and
    the user is classified as underage.
    """
    invalid_format = "27.08.2007"

    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup

    # Submit birthdate with invalid format
    popup.submit_birthdate(invalid_format)

    # Invalid input should trigger a warning
    assert popup.is_warning_message_displayed(), (
        "An invalid date format should trigger a warning message."
    )
