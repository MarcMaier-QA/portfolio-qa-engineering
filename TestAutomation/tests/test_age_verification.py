import pytest

from TestAutomation.pages.home_page import HomePage

@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_allows_access_to_alcohol(login):
    """
    COMPLIANCE TEST: TC-04
    Adult users gain access to alcoholic products.
    """
    user_is_over_eighteen = "27-08-2007"

    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup
    assert popup.is_popup_displayed(), "The age popup did not appear.."

    popup.submit_birthdate(user_is_over_eighteen)
    assert popup.is_success_message_displayed(), "'You are of age' should be visible. "

    # Zugriff auf Alkoholkategorie
    shop.filter_alcohol()

    shop.wait_until_shop_ready()

    assert shop.has_visible_products(), \
        "Alcohol products should be visible for users +18 old. "


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_blocks_underage_user(login):
    """
    COMPLIANCE TEST: TC-05
    Underage users must not have access to alcoholic products.
    """
    user_is_under_eighteen = "27-08-2015"

    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup
    assert popup.is_popup_displayed(), "Age verification popup should be visible. "

    popup.submit_birthdate(user_is_under_eighteen)
    assert popup.is_warning_message_displayed(), (
        "Warning message should be displayed for underage user. "
    )

    # Zugriff auf Alkoholkategorie
    shop.filter_alcohol()

    # Erwartung: Underage Notice sichtbar
    assert shop.is_underage_notice_visible(), \
        "Underage notice should be visible in alcohol category. "

    # Absicherung: keine Alkoholprodukte sichtbar
    assert not shop.has_visible_products(), \
        "No alcohol products should be visible for underage users. "


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_without_birthdate_shows_error(login):
    """
    COMPLIANCE TEST: TC-06
    Confirming age verification without a date will classify the user as a minor.
    """
    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup

    popup.click_confirm()
    assert popup.is_warning_message_displayed(), (
        "Error message should appear when no birthdate is entered. "
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_invalid_date_format(login):
    """
    TC-07:
    Invalid date formats will not be accepted and the user will be classified as a minor.
    """
    invalid_format = "27.08.2007"

    home = HomePage(login)
    shop = home.go_to_shop()

    popup = shop.age_popup

    popup.submit_birthdate(invalid_format)
    assert popup.is_warning_message_displayed(), (
        "Invalid date format should trigger warning message. "
    )
