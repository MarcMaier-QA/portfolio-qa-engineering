import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

VALID_PASSWORD = "secret_sauce"
USERS = [
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
]

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()


@pytest.mark.parametrize("username", USERS)
def test_login(driver, username):
    # Eingabefelder finden
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # Daten eingeben
    username_field.send_keys(username)
    password_field.send_keys(VALID_PASSWORD)

    # Login ausführen
    login_button.click()

    # Login prüfen
    title_element = driver.find_element(By.CLASS_NAME, "title")
    assert title_element.text == "Products"