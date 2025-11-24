from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


USER_DATA = {
    "account_information": {
        "title_id": "id_gender1",
        "name": "Günter",
        "email": "test@test32567.de",
        "password": "testcaseone",
        "birth_day": "27",
        "birth_month": "8",
        "birth_year": "2007"
    },
    "address_information": {
        "first_name": "Marc",
        "last_name": "Mctester",
        "company": "Masterschool",
        "address": "teststreet.14",
        "country": "India",
        "state": "testenhausen",
        "city": "teststadt",
        "zipcode": "12345",
        "mobile_number": "012345631278"
    }
}

# Aufgabe 3 (Benutzer registrieren)
def test_benutzer_registrieren():
    driver = webdriver.Chrome()
    driver.get("http://automationexercise.com")

    # Cookie-Banner schließen
    try:
        einwilligen_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(),'Einwilligen')]/ancestor::button"))
        )
        einwilligen_btn.click()

        # Warten bis Overlay weg ist
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fc-dialog-overlay"))
        )

    except TimeoutException:
        pass


    # Warten, bis das Logo sichtbar ist (bis zu 10 Sekunden)
    logo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//img[@alt='Website for automation practice']"))
    )

    # Überprüft das logo
    assert logo.is_displayed()

    # Signup / Login-Button finden
    driver.find_element(By.XPATH, "//a[text()=' Signup / Login']").click()

    # Überprüfen das wir 'New User Signup!' sehen
    signup_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='New User Signup!']"))
    )

    # Überprüft den titel New User Signup!
    assert signup_title.is_displayed()

    # Signup-Felder finden
    # Namens-Feld
    driver.find_element(By.XPATH, "//input[@data-qa='signup-name']").send_keys(
        USER_DATA["account_information"]["name"]
    )

    # E-Mail-Feld
    driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys(
        USER_DATA["account_information"]["email"]
    )

    # Signup-Button klicken
    driver.find_element(By.XPATH, "//button[@data-qa='signup-button']").click()

    # Überprüfen das wir 'Enter Account Information' sehen
    account_info_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2/b[text()='Enter Account Information']"))
    )

    # Überprüft den titel Enter Account Information
    assert account_info_title.is_displayed(), "Titel 'Enter Account Information' NICHT gefunden!"

    # Titel auswählen
    driver.find_element(By.ID, USER_DATA["account_information"]["title_id"]).click()

    # Password eingeben
    driver.find_element(By.ID, "password").send_keys(USER_DATA["account_information"]["password"])

    # Dropdowns auswählen
    # Tag
    day_select = Select(driver.find_element(By.ID, "days"))
    day_select.select_by_value(USER_DATA["account_information"]["birth_day"])

    # Monat
    month_select = Select(driver.find_element(By.ID, "months"))
    month_select.select_by_value(USER_DATA["account_information"]["birth_month"])

    # Jahr
    year_select = Select(driver.find_element(By.ID, "years"))
    year_select.select_by_value(USER_DATA["account_information"]["birth_year"])

    # Checkbox "Newsletter"
    newsletter_checkbox = driver.find_element(By.ID, "newsletter")
    if not newsletter_checkbox.is_selected():
        newsletter_checkbox.click()

    # Checkbox "Optin"
    optin_checkbox = driver.find_element(By.ID, "optin")
    if not optin_checkbox.is_selected():
        optin_checkbox.click()

    # Address Information ausfüllen
    # First Name
    driver.find_element(By.ID, "first_name").send_keys(USER_DATA["address_information"]["first_name"])

    # Last Name
    driver.find_element(By.ID, "last_name").send_keys(USER_DATA["address_information"]["last_name"])

    # Company
    driver.find_element(By.ID, "company").send_keys(USER_DATA["address_information"]["company"])

    # Address
    driver.find_element(By.ID, "address1").send_keys(USER_DATA["address_information"]["address"])

    # Country (Dropdown)
    country_select = Select(driver.find_element(By.ID, "country"))
    country_select.select_by_visible_text(USER_DATA["address_information"]["country"])

    # State
    driver.find_element(By.ID, "state").send_keys(USER_DATA["address_information"]["state"])

    # City
    driver.find_element(By.ID, "city").send_keys(USER_DATA["address_information"]["city"])

    # Zipcode
    driver.find_element(By.ID, "zipcode").send_keys(USER_DATA["address_information"]["zipcode"])

    # Mobile Number
    driver.find_element(By.ID, "mobile_number").send_keys(USER_DATA["address_information"]["mobile_number"])

    # Create Account anklicken
    driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

    # Überprüft den titel: account-created!
    account_created = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-created']"))
    )

    assert account_created.is_displayed(), "Account wurde NICHT erfolgreich erstellt!"

    # Continue anklicken
    driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

    logged_in_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Logged in as')]"))
    )

    # Jetzt den Namen auslesen
    logged_in_name = driver.find_element(By.XPATH, "//a[contains(text(), 'Logged in as')]/b").text

    assert logged_in_name == USER_DATA["account_information"]["name"], ""

    # Delete account anklicken
    driver.find_element(By.XPATH, "//a[@href='/delete_account']").click()

    # Überprüfen ob account gelöscht
    deleted_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[@data-qa='account-deleted']"))
    )

    assert deleted_msg.is_displayed(), "Account wurde NICHT erfolgreich gelöscht!"

    # Continue anklicken
    driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

    driver.quit()