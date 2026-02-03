from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)

    def open(self, url: str):
        """
        Navigates to the given URL and returns the page instance
        to allow method chaining.
        """
        self.driver.get(url)
        return self

    def click(self, locator):
        """
        Clicks on an element after waiting until it becomes clickable.
        This ensures stability and avoids timing issues.
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str, clear: bool = True):
        """
        Types text into an input field.
        Optionally clears the field beforehand (default behavior).
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def is_visible(self, locator) -> bool:
        """
        Checks whether an element is visible on the page.
        Uses find_elements instead of try/except to avoid exceptions.
        """
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    def is_present(self, locator, timeout: int = None) -> bool:
        """
        Checks whether an element is present in the DOM.
        Uses find_elements to avoid raising exceptions.
        A temporary implicit wait is applied for flexibility.
        """
        time = timeout if timeout else DEFAULT_WAIT_TIME

        # Temporarily enable implicit wait
        self.driver.implicitly_wait(time)
        elements = self.driver.find_elements(*locator)
        # Disable implicit wait immediately (best practice)
        self.driver.implicitly_wait(0)

        return len(elements) > 0

    def get_text(self, locator) -> str:
        """
        Returns the visible text of an element.
        Waits until the element is visible before accessing the text.
        """
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def get_element(self, locator):
        """
        Returns a WebElement once it becomes visible.
        Useful when further interactions are required.
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator):
        """
        Returns all matching elements.
        Waits until at least one element is present in the DOM.
        """
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def find_elements_no_wait(self, locator):
        """
        Returns elements without applying any wait.
        Intended for quick existence checks.
        """
        return self.driver.find_elements(*locator)

    def wait_until_not_visible(self, locator):
        """
        Waits until an element is no longer visible.
        Commonly used for loaders, overlays or toast messages.
        """
        self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text_change(self, locator, old_text: str):
        """
        Waits until the text of an element changes from the given value.
        Useful for dynamic content updates.
        """
        self.wait.until_not(EC.text_to_be_present_in_element(locator, old_text))
