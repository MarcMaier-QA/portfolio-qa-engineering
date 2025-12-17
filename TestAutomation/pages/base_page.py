from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)

    def open(self, url: str):
        """Navigiert zu einer URL"""
        self.driver.get(url)
        return self

    def click(self, locator):
        """Klickt auf ein Element, nachdem es klickbar ist"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str, clear: bool = True):
        """Gibt Text in ein Eingabefeld ein"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def is_visible(self, locator) -> bool:
        """Prüft, ob ein Element sichtbar ist (Ohne Try-Except)"""
        # Wir warten, bis Selenium das Element im DOM findet
        self.wait.until(EC.presence_of_element_located(locator))
        elements = self.driver.find_elements(*locator)
        if elements:
            return elements[0].is_displayed()
        return False

    def is_present(self, locator, timeout: int = None) -> bool:
        """
        Prüft, ob ein Element im DOM vorhanden ist.
        Nutzt find_elements, um Exceptions zu vermeiden.
        """
        time = timeout if timeout else DEFAULT_WAIT_TIME

        self.driver.implicitly_wait(time)  # Kurzzeitig implizites Warten einschalten
        elements = self.driver.find_elements(*locator)
        self.driver.implicitly_wait(0)  # Sofort wieder ausschalten (Best Practice)

        return len(elements) > 0

    def get_text(self, locator) -> str:
        """Gibt den Text eines Elements zurück"""
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def get_element(self, locator):
        """Gibt das WebElement zurück, sobald es sichtbar ist"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator):
        """Gibt alle passenden Elemente zurück (wartet bis mindestens eines da ist)"""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def find_elements_no_wait(self, locator):
        """Gibt Elemente zurück ohne zu warten (für Checks, ob Element existiert)"""
        return self.driver.find_elements(*locator)

    def wait_until_not_visible(self, locator):
        """Wartet, bis ein Element nicht mehr sichtbar ist"""
        self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_text_change(self, locator, old_text: str):
        """Wartet, bis sich der Text eines Elements ändert"""
        self.wait.until_not(EC.text_to_be_present_in_element(locator, old_text))