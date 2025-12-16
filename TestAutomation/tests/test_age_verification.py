import pytest
from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.pages.product_page import ProductPage
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.utils.constants import PRODUCT_IGNIS_VODKA_URL, PRODUCT_IGNIS_VODKA_NAME


@pytest.mark.ui
@pytest.mark.compliance
@pytest.mark.parametrize("birthdate", ["27-08-2007"])
def test_age_verification_allows_access_to_alcohol(login, birthdate):
    """
    COMPLIANCE TEST:
    Adult users should be able to access alcohol products
    after successful age verification via the shop flow.
    """

    shop = ShopPage(login)
    popup = AgeVerificationPopup(login)
    product = ProductPage(login)

    # GIVEN
    shop.open_shop()
    assert popup.is_popup_displayed()

    # WHEN
    popup.submit_birthdate(birthdate)

    # THEN
    assert popup.is_success_message_displayed()

    product.open(PRODUCT_IGNIS_VODKA_URL)
    assert product.is_product_name_displayed(PRODUCT_IGNIS_VODKA_NAME)


@pytest.mark.ui
@pytest.mark.compliance
def test_underage_user_sees_underage_notice_when_filtering_alcohol(login):
    """
    COMPLIANCE TEST:
    Underage users must see an explicit 'Underage Notice'
    when attempting to access alcohol products via the shop filter.
    """

    shop = ShopPage(login)
    popup = AgeVerificationPopup(login)

    # GIVEN
    shop.open_shop()
    assert popup.is_popup_displayed()

    # WHEN
    popup.submit_birthdate("27-08-2008")
    assert popup.is_warning_message_displayed()

    shop.filter_alcohol()

    # THEN
    assert shop.is_underage_notice_visible(), (
        "COMPLIANCE BUG: Underage notice not displayed for alcohol filter"
    )



@pytest.mark.security
def test_direct_url_access_bypasses_age_verification(driver):
    """
    SECURITY BUG:
    Alcohol product page is accessible via direct URL
    without prior age verification.
    """

    product = ProductPage(driver)

    # WHEN
    product.open(PRODUCT_IGNIS_VODKA_URL)
    product.wait_until_loaded()

    # THEN
    assert product.is_product_name_displayed(PRODUCT_IGNIS_VODKA_NAME)
