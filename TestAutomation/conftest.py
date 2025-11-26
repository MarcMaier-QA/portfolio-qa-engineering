import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login_email = "test@test32567.de"
password_user = "test123"

@pytest.fixture
def driver():
    """Startet ChromeDriver vor jedem Test und schließt ihn danach."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


@pytest.fixture
def login(driver):
    """Loggt einen gültigen Nutzer für alle Tests ein."""
    driver.get("https://grocerymate.masterschool.com/auth")

    # Email-Feld
    email = driver.find_element(By.XPATH, "//input[@placeholder='Email address']")

    # Passwort-Feld
    password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

    # Login-Button
    login_btn = driver.find_element(By.XPATH, "//button[contains(.,'Sign In')]")

    # Eingeben
    email.send_keys(login_email)
    password.send_keys(password_user)
    login_btn.click()

    # Warten, bis der Shop geladen ist
    WebDriverWait(driver, 10).until(
        EC.url_to_be( "https://grocerymate.masterschool.com/")
    )

    return driver
