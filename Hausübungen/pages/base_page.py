from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Gemeinsame Basis für alle PageObjects"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Basic Actions
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator, text):
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.visible(locator).text

    # Checks
    def is_visible(self, locator):
        try:
            self.visible(locator)
            return True
        except Exception as e:
            return False, f"Fehler: {e}"

    def assert_visible(self, locator, msg="Element not visible"):
        """Standard Assertion für Sichtbarkeit"""
        assert self.is_visible(locator), msg

    # Utility
    def scroll_to(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def scroll_and_click(self, locator):
        element = self.scroll_to(locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()
