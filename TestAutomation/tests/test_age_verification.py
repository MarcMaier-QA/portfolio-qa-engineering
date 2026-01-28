import pytest

from TestAutomation.pages.product_page import ProductPage
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.utils.constants import PRODUCT_IGNIS_VODKA_NAME


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_allows_access_to_alcohol(login):
    """
    COMPLIANCE TEST: TC-04
    Volljährige Nutzer erhalten Zugriff auf Alkoholprodukte.
    """
    user_is_over_eighteen = "27-08-2007"

    shop = ShopPage(login).open()
    shop.verify_age_as_adult(user_is_over_eighteen)

    product = ProductPage(login).open_ignis_vodka()
    assert product.has_product_name(PRODUCT_IGNIS_VODKA_NAME)


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_blocks_underage_user(login):
    """
    COMPLIANCE TEST: TC-05
    Minderjährige Nutzer dürfen keinen Zugriff auf Alkoholprodukte erhalten.
    """
    user_is_under_eighteen = "27-08-2015"

    shop = ShopPage(login).open()
    shop.verify_age_as_minor(user_is_under_eighteen)


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_without_birthdate_shows_error(login):
    """
    COMPLIANCE TEST: TC-06
    Altersverifikation darf nicht ohne Geburtsdatum bestätigt werden.
    """

    shop = ShopPage(login).open()
    shop.verify_age_without_birthdate()


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_invalid_date_format(login):
    """
    COMPLIANCE TEST: TC-07
    Ungültiges Datumsformat (DD.MM.YYYY) darf nicht akzeptiert werden.
    """
    invalid_format = "27.08.2007"

    shop = ShopPage(login).open()
    shop.verify_age_with_invalid_date_format(invalid_format)
