import pytest
from pages.shop_page import ShopPage
from pages.age_verification_popup import AgeVerificationPopup


@pytest.mark.parametrize("birthdate, expected_result", [
    ("27-08-2007", "success"),   # TC-04: ~18 Jahre = Zugang erlaubt
    ("27-08-2008", "warning"),   # TC-05: ~17 Jahre = Zugang verweigert
    ("", "warning"),             # TC-06: DD-MM-YYYY leer = warning
    ("27.08.2007", "warning"),   # TC-07: Falsches Format = warning
])

def test_age_verification(login, birthdate, expected_result):
    driver = login

    shop_page = ShopPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # 1. Aktion: Shop öffnen (Link ist in ShopPage)
    shop_page.click_shop_button()

    # 2. Aktion: Datum eingeben und bestätigen (Logik ist in AgeVerificationPopup)
    age_popup.enter_birthdate_and_confirm(birthdate)

    # 3. Assertion: Verhalten prüfen
    if expected_result == "success":
        assert age_popup.is_success_message_displayed(), \
            f"TC-04 fehlgeschlagen: Erwartete Erfolgsmeldung nicht gefunden für Datum {birthdate}"
    else:
        assert age_popup.is_warning_message_displayed(), \
            f"TC-05/06/07 fehlgeschlagen: Erwartete Warnmeldung nicht gefunden für Datum {birthdate}"
