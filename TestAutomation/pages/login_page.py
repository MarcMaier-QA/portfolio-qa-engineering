from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from TestAutomation.utils.constants import DEFAULT_WAIT_TIME


class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Locators
        self.EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Email address']")
        self.PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
        self.LOGIN_BUTTON = (By.XPATH, "//button[contains(.,'Sign In']")
        self.HOME_PAGE_IDENTIFIER = (By.XPATH, "//a[@href='/store' and text()='Shop']")


    def login(self, email: str, password: str):
        """Führt die Anmeldung aus."""

        # 1. Warten und E-Mail eingeben
        email_field = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.element_to_be_clickable(self.EMAIL_INPUT)
        )
        email_field.send_keys(email)

        # 2. Password eingeben
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

        # 3. Anmelden klicken
        self.driver.find_element(*self.LOGIN_BUTTON).click()

        # 4. Warten auf den wechsel/ das Laden der seite
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.HOME_PAGE_IDENTIFIER)
        )
