import pytest
from TestAutomation.pages.age_verification_popup import AgeVerificationPopup
from TestAutomation.pages.product_page import ProductPage
from TestAutomation.pages.shop_page import ShopPage
from TestAutomation.utils.constants import (
    PRODUCT_IGNIS_VODKA_URL,
    PRODUCT_IGNIS_VODKA_NAME
)
# todo: parametrize raus

@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_allows_access_to_alcohol(login):
    """
    COMPLIANCE TEST: TC-04

    Szenario:
    Volljährige Nutzer (18+) sollen nach erfolgreicher Altersverifikation
    Zugang zu alkoholischen Produkten erhalten.

    Ablauf:
    1. Shop öffnen
    2. Altersverifikations-Popup erscheint
    3. Volljähriges Geburtsdatum eingeben
    4. Erfolgsmeldung wird angezeigt
    5. Alkoholprodukt ist zugänglich

    Erwartetes Verhalten:
    - Popup wird angezeigt
    - Erfolgsmeldung erscheint nach Eingabe
    - Produktseite ist erreichbar und zeigt korrekten Namen
    """
    birthdate = "27-08-2007"

    shop_page = ShopPage(login)
    age_popup = AgeVerificationPopup(login)
    product_page = ProductPage(login)

    # 1. Shop öffnen
    shop_page.navigate_to_shop()

    # 2. Prüfe ob Altersverifikations-Popup angezeigt wird
    assert age_popup.is_popup_displayed(), (
        "Altersverifikations-Popup wird nicht angezeigt beim Öffnen des Shops"
    )

    # 3. Geburtsdatum eingeben und bestätigen
    age_popup.submit_birthdate(birthdate)

    # 4. Prüfe ob Erfolgsmeldung angezeigt wird
    assert age_popup.is_success_message_displayed(), (
        f"Erfolgsmeldung wird nicht angezeigt nach Eingabe von: {birthdate}. "
        f"Tatsächliche Nachricht: {age_popup.get_success_message_text()}"
    )

    # 5. Navigiere zu alkoholischem Produkt
    product_page.navigate_to(PRODUCT_IGNIS_VODKA_URL)

    # 6. Prüfe ob Produktname korrekt angezeigt wird
    assert product_page.is_product_name_displayed(PRODUCT_IGNIS_VODKA_NAME), (
        f"Produktname '{PRODUCT_IGNIS_VODKA_NAME}' wird nicht korrekt angezeigt. "
        f"Tatsächlicher Titel: {product_page.get_text(product_page.PRODUCT_TITLE)}"
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_underage_user_sees_underage_notice_when_filtering_alcohol(login):
    """
    COMPLIANCE TEST: TC-05

    Szenario:
    Minderjährige Nutzer (unter 18) müssen explizit darauf hingewiesen werden,
    dass sie keinen Zugriff auf alkoholische Produkte haben.

    Ablauf:
    1. Shop öffnen
    2. Altersverifikations-Popup erscheint
    3. Minderjähriges Geburtsdatum eingeben (z.B. 2008)
    4. Warnmeldung wird angezeigt
    5. Alkohol-Filter anklicken
    6. "Underage Notice" wird angezeigt

    Erwartetes Verhalten:
    - Warnmeldung erscheint nach Eingabe
    - Underage Notice wird im Shop angezeigt
    - Zugriff auf Alkoholprodukte ist blockiert
    """
    driver = login
    shop_page = ShopPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # 1. Shop öffnen
    shop_page.navigate_to_shop()

    # 2. Prüfe ob Altersverifikations-Popup angezeigt wird
    assert age_popup.is_popup_displayed(), (
        "Altersverifikations-Popup wird nicht angezeigt beim Öffnen des Shops"
    )

    # 3. Minderjähriges Geburtsdatum eingeben (2008 = unter 18)
    underage_birthdate = "27-08-2008"
    age_popup.submit_birthdate(underage_birthdate)

    # 4. Prüfe ob Warnmeldung angezeigt wird
    assert age_popup.is_warning_message_displayed(), (
        f"Warnmeldung wird nicht angezeigt nach Eingabe von: {underage_birthdate}. "
        f"Tatsächliche Nachricht: {age_popup.get_warning_message_text()}"
    )

    # 5. Versuche Alkohol-Filter anzuwenden
    shop_page.filter_alcohol()

    # 6. Prüfe ob "Underage Notice" angezeigt wird
    assert shop_page.is_underage_notice_visible(), (
        "COMPLIANCE BUG: 'Underage Notice' wird nicht angezeigt, obwohl User minderjährig ist. "
        "Minderjährige könnten potenziell Alkohol sehen!"
    )


@pytest.mark.security
@pytest.mark.xfail(
    reason="SECURITY BUG: Direkter URL-Zugriff auf Alkoholprodukte umgeht Altersverifikation"
)
def test_direct_url_access_bypasses_age_verification(driver):
    """
    SECURITY BUG TEST: TC-06

    Kritischer Sicherheitsmangel:
    Die Altersverifikation kann durch direkten URL-Zugriff umgangen werden.

    Szenario:
    1. OHNE Login oder Altersverifikation
    2. Direkt zur Alkoholprodukt-URL navigieren
    3. Produktseite ist zugänglich

    Aktuelles Verhalten (BUG):
    - Produktseite wird ohne Alterscheck angezeigt
    - Minderjährige könnten Alkohol kaufen

    Erwartetes Verhalten (nach Fix):
    - Altersverifikations-Popup sollte erscheinen
    - Oder Zugriff sollte verweigert werden
    - Redirect zu Shop mit Popup

    Compliance-Risiko:
    Dies ist ein kritischer Verstoß gegen Jugendschutzgesetze!
    """
    product_page = ProductPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # WHEN: Direkter Zugriff auf Alkoholprodukt via URL (ohne vorherige Verifikation)
    product_page.navigate_to(PRODUCT_IGNIS_VODKA_URL)

    # THEN (BUG): Produkt ist direkt zugänglich
    assert product_page.is_product_name_displayed(PRODUCT_IGNIS_VODKA_NAME), (
        "Produkt sollte zugänglich sein (Bug-Bestätigung)"
    )

    # EXPECTED BEHAVIOR (nach Fix): Popup sollte erscheinen
    # assert age_popup.is_popup_displayed(), (
    #     "Altersverifikations-Popup sollte erscheinen bei direktem URL-Zugriff"
    # )

    # ODER: Zugriff sollte verweigert werden
    # assert not product_page.is_product_name_displayed(PRODUCT_IGNIS_VODKA_NAME), (
    #     "Alkoholprodukt sollte NICHT ohne Altersverifikation zugänglich sein"
    # )


@pytest.mark.ui
@pytest.mark.compliance
@pytest.mark.parametrize("birthdate,expected_result,test_case", [
    ("", "underage", "TC-06: Leeres Eingabefeld"),
    ("27.08.2007", "underage", "TC-07: Falsches Datumsformat (Punkte statt Bindestriche)"),
    ("2007-08-27", "underage", "TC-07b: Falsches Datumsformat (ISO Format)"),
    ("27/08/2007", "underage", "TC-07c: Falsches Datumsformat (Slashes)"),
])
def test_invalid_birthdate_input_treats_user_as_underage(login, birthdate, expected_result, test_case):
    """
    COMPLIANCE TEST: TC-06 & TC-07

    Parametrisierter Test für ungültige Geburtsdatum-Eingaben.

    Testfälle:
    - TC-06: Leeres Eingabefeld
    - TC-07: Falsches Datumsformat (verschiedene Varianten)

    Szenario:
    Bei ungültigen Eingaben (leer oder falsches Format) sollte der Nutzer
    als minderjährig behandelt werden (fail-safe Verhalten).

    Erwartetes Verhalten:
    - Warnmeldung erscheint
    - Nutzer wird als unter 18 behandelt
    - Zugriff auf Alkohol wird verweigert
    """
    driver = login
    shop_page = ShopPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # 1. Shop öffnen
    shop_page.navigate_to_shop()

    # 2. Prüfe ob Popup angezeigt wird
    assert age_popup.is_popup_displayed(), (
        f"{test_case}: Altersverifikations-Popup wird nicht angezeigt"
    )

    # 3. Ungültige Eingabe abschicken
    if birthdate == "":
        # Für leeres Feld: Nur Button klicken ohne Eingabe
        age_popup.click_confirm()
    else:
        # Für falsche Formate: Eingabe machen und bestätigen
        age_popup.submit_birthdate(birthdate)

    # 4. Prüfe ob Warnmeldung erscheint (fail-safe: behandle als minderjährig)
    assert age_popup.is_warning_message_displayed(), (
        f"{test_case}: Warnmeldung wird nicht angezeigt bei ungültiger Eingabe '{birthdate}'. "
        f"Tatsächliche Nachricht: {age_popup.get_warning_message_text()}"
    )

    # 5. Zusätzlicher Check: Versuche Alkohol-Filter
    shop_page.filter_alcohol()

    # 6. Prüfe ob "Underage Notice" angezeigt wird
    assert shop_page.is_underage_notice_visible(), (
        f"{test_case}: 'Underage Notice' wird nicht angezeigt. "
        f"Bei ungültiger Eingabe '{birthdate}' sollte Zugriff verweigert werden!"
    )


@pytest.mark.ui
@pytest.mark.compliance
def test_age_verification_popup_appears_on_shop_access(login):
    """
    COMPLIANCE TEST: Basis-Check

    Basis-Test zur Sicherstellung, dass das Altersverifikations-Popup
    beim Zugriff auf den Shop erscheint.

    Erwartetes Verhalten:
    - Popup erscheint automatisch beim Shop-Zugriff
    - Eingabefeld für Geburtsdatum ist sichtbar
    - Confirm-Button ist vorhanden
    """
    driver = login
    shop_page = ShopPage(driver)
    age_popup = AgeVerificationPopup(driver)

    # Shop öffnen
    shop_page.navigate_to_shop()

    # Prüfe dass Popup erscheint
    assert age_popup.is_popup_displayed(), (
        "Altersverifikations-Popup erscheint nicht beim Shop-Zugriff"
    )

    # Prüfe dass alle wichtigen Elemente sichtbar sind
    assert age_popup.is_date_input_visible(), (
        "Datumseingabefeld ist nicht sichtbar im Popup"
    )