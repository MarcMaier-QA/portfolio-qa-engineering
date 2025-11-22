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
# Setup: Browser starten
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
# Names-Feld
driver.find_element(By.XPATH, "//input[@data-qa='signup-name']").send_keys(USER_DATA["account_information"]["name"])

# E-Mail-Feld
driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys(USER_DATA["account_information"]["email"])

# Signup-Button klicken
driver.find_element(By.XPATH, "//button[@data-qa='signup-button']").click()

# Überprüfen das wir 'Enter Account Information' sehen
account_info_title = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Enter Account Information']"))
)

# Überprüft den titel Enter Account Information
assert account_info_title.is_displayed()

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