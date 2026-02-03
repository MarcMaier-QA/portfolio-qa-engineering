from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, LOGIN_URL


class LoginPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Locators
        # Defined inside the page object to keep selectors close to the page structure
        self.EMAIL_INPUT = (By.XPATH, "//input[@placeholder='Email address']")
        self.PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='Password']")
        self.LOGIN_BUTTON = (By.XPATH, "//button[contains(.,'Sign In')]")

        # Element that reliably identifies a successful login
        # Used instead of URL checks to reflect real user-visible state
        self.HOME_PAGE_IDENTIFIER = (By.XPATH, "//a[@href='/store' and text()='Shop']")

    def navigate_to_login(self, url: str = LOGIN_URL):
        """
        Navigates directly to the login page.

        Direct URL navigation is intentionally used here to speed up test setup.
        This avoids unnecessary UI steps when the test focus is authentication itself.
        """
        self.driver.get(url)

        # Wait until the login form is ready for interaction
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )

    def login(self, email: str, password: str):
        """
        Performs the login action using provided credentials.

        The method waits for each critical step to ensure stability
        and verifies success via a visible home page element.
        """

        # 1. Wait for the email field to be interactable and enter the email
        email_field = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.element_to_be_clickable(self.EMAIL_INPUT)
        )
        email_field.send_keys(email)

        # 2. Enter password (field is expected to be present after email is ready)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

        # 3. Submit the login form
        self.driver.find_element(*self.LOGIN_BUTTON).click()

        # 4. Wait for a user-visible element that confirms successful login
        # This is more reliable than waiting for a URL change
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.HOME_PAGE_IDENTIFIER)
        )
