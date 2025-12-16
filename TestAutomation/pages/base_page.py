from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)

    def open(self, url: str):
        self.driver.get(url)
        return self

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str, clear: bool = True):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def is_visible(self, locator) -> bool:
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()

    def is_present(self, locator) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_text(self, locator) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text
