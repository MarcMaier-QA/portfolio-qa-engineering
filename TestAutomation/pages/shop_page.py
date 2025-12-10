from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, SHOP_URL
import time


class ShopPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.SHOP_BUTTON = (By.XPATH, "//a[text()='Shop']")
        self.PRODUCT_CARD_GENERAL = (By.XPATH, "//div[contains(@class,'product-card')]")
        self.PRODUCT_CARD_BY_NAME = lambda name: (
            By.XPATH,
            f"//p[@class='lead' and text()='{name}']/ancestor::div[contains(@class,'product-card')]"
        )
        self.QUANTITY_INPUT = (By.XPATH, ".//input[@type='number']")
        self.ADD_TO_CARD_BUTTON = (By.XPATH, ".//button[contains(@class,'btn-cart')]")
        self.NEXT_PAGE_BUTTON = (By.XPATH, "//button[contains(@class,'pagination-link') and text()='Next']")

    # Navigationsmethoden
    def navigate_to_shop(self):
        """Navigiert direkt zur Shop-Seite per URL"""
        self.driver.get(SHOP_URL)
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located(self.PRODUCT_CARD_GENERAL)
        )

    def click_shop_button(self):
        """Klickt den 'Shop'-Link an"""
        shop_btn = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.element_to_be_clickable(self.SHOP_BUTTON)
        )
        shop_btn.click()
        # Warte auf die Zielseite
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.presence_of_element_located(self.PRODUCT_CARD_GENERAL)
        )

    # Produktinteraktion
    def find_product_card(self, product_name: str, timeout: int = DEFAULT_WAIT_TIME ) -> WebElement | None:
        """Findet ein Produkt auf allen Shop-Seiten"""
        wait = WebDriverWait(self.driver, timeout)
        while True:
            cards = self.driver.find_elements(*self.PRODUCT_CARD_BY_NAME(product_name))
            if cards:
                return cards[0] # Gibt Webelement zurück

            next_buttons = self.driver.find_elements(*self.NEXT_PAGE_BUTTON)

            # WICHTIG: Wenn das Produkt nicht gefunden wird, muss der Test fehlschlagen.
            # Wir werfen eine Exception, anstatt None zurückzugeben.
            if not next_buttons or "disabled" in next_buttons[0].get_attribute("class"):
                raise Exception(f"Product '{product_name}' not found after searching all pages.")

            next_buttons[0].click()
            wait.until(EC.presence_of_element_located(self.PRODUCT_CARD_GENERAL))
            time.sleep(0.3)

    def add_product_to_cart(self, product_name: str, quantity: int):
        """Sucht das Produkt, setzt die Menge und fügt es dem Wahrenkorb hinzu"""
        # find_product_card wirft Exception, wenn nicht gefunden
        product_card = self.find_product_card(product_name)

        # Logik für die Interaktion mit der gefundenen Produktkarte
        quantity_input = product_card.find_element(*self.QUANTITY_INPUT)
        add_btn = product_card.find_element(*self.ADD_TO_CARD_BUTTON)

        quantity_input.clear()
        time.sleep(0.2)
        for digit in str(quantity):
            quantity_input.send_keys(digit)
            time.sleep(0.1)

        add_btn.click()
        time.sleep(1)

        current_quantity = int(quantity_input.get_attribute("value"))
        if current_quantity != quantity:
            quantity_input.clear()
            for digit in str(quantity):
                quantity_input.send_keys(digit)
                time.sleep(0.1)
            add_btn.click()
            time.sleep(1)
