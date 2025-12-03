import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize("birthdate, expected_result", [
    ("27-08-2007", "success"),   # TC-04: ~18 Jahre = Zugang erlaubt
    ("27-08-2008", "warning"),   # TC-05: ~17 Jahre = Zugang verweigert
    ("", "warning"),             # TC-06: DD-MM-YYYY leer = warning
])


def test_age_verification(login, birthdate, expected_result):
    driver = login

    # In den Shop navigieren
    shop_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Shop']"))
    )
    shop_btn.click()

    # Alters-Popup abwarten
    date_input = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='DD-MM-YYYY']"))
    )
    date_input.clear()
    if birthdate:
        date_input.send_keys(birthdate)

    # Bestätigen
    confirm_btn = driver.find_element(By.XPATH, "//button[text()='Confirm']")
    confirm_btn.click()

    # Erwartetes Verhalten prüfen
    if expected_result == "success":
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'You are of age')]"))
        )
    else:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'You are underage')]"))
        )
