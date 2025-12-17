from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage
from TestAutomation.utils.constants import SHOP_URL


class ShopPage(BasePage):
    # Navigation / Filters
    SHOP_BUTTON = (By.XPATH, "//a[text()='Shop']")
    ALCOHOL_FILTER = (By.XPATH, "//a[normalize-space()='Alocohol']")
    UNDERAGE_NOTICE = (By.XPATH, "//h2[normalize-space()='Underage Notice']")

    # Products
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class,'product-card')]")

    def PRODUCT_CARD_BY_NAME(self, name: str):
        """Dynamischer Locator für eine spezifische Produktkarte"""
        return (
            By.XPATH,
            f"//p[@class='lead' and normalize-space()='{name}']"
            f"/ancestor::div[contains(@class,'product-card')]"
        )

    # Product actions
    QUANTITY_INPUT = (By.XPATH, ".//input[@type='number']")
    ADD_TO_CART_BUTTON = (By.XPATH, ".//button[contains(@class,'btn-cart')]")

    # Pagination
    NEXT_PAGE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'pagination-link') and normalize-space()='Next']"
    )

    # Navigation
    def navigate_to_shop(self):
        """Öffnet den Shop ohne auf Produkte zu warten (da Popup zuerst kommt)"""
        self.open(SHOP_URL)

    def click_shop_button(self):
        """Navigiert zum Shop über den Header-Button"""
        self.click(self.SHOP_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))

    def filter_alcohol(self):
        """Klickt auf den Alkohol-Filter"""
        self.click(self.ALCOHOL_FILTER)
        self.wait.until(EC.presence_of_element_located(self.UNDERAGE_NOTICE))

    # Product search (OHNE while-Schleife!)
    def find_product_card(self, product_name: str, max_pages: int = 10) -> WebElement | None:
        """
        Sucht ein Produkt über mehrere Seiten hinweg.
        Nutzt rekursive Logik statt while-Schleife.

        Args:
            product_name: Name des Produkts
            max_pages: Maximale Anzahl an Seiten die durchsucht werden

        Returns:
            WebElement der Produktkarte oder None
        """
        return self._find_product_recursive(product_name, pages_searched=0, max_pages=max_pages)

    def _find_product_recursive(self, product_name: str, pages_searched: int, max_pages: int) -> WebElement | None:
        """
        Hilfsmethode: Rekursive Produktsuche über Seiten.
        """
        # Abbruchbedingung 1: Max Seiten erreicht
        if pages_searched >= max_pages:
            return None

        # Suche auf aktueller Seite
        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        if cards:
            return cards[0]

        # Abbruchbedingung 2: Keine nächste Seite verfügbar
        if not self.has_next_page():
            return None

        # Gehe zur nächsten Seite
        self.go_to_next_page()

        # Rekursiver Aufruf für nächste Seite
        return self._find_product_recursive(product_name, pages_searched + 1, max_pages)

    def is_product_visible(self, product_name: str) -> bool:
        """
        Prüft, ob ein Produkt auf der AKTUELLEN Seite sichtbar ist.
        Keine Pagination!
        """
        cards = self.find_elements_no_wait(self.PRODUCT_CARD_BY_NAME(product_name))
        return len(cards) > 0

    # Product actions
    def add_product_to_cart(self, product_name: str, quantity: int):
        """
        Fügt ein Produkt mit bestimmter Menge zum Warenkorb hinzu.
        Sucht das Produkt automatisch über alle Seiten.
        """
        # 1. Finde die Produktkarte
        product_card = self.find_product_card(product_name)

        # 2. Assertion: Produkt muss gefunden werden
        assert product_card is not None, f"Produkt '{product_name}' wurde nicht im Shop gefunden"

        # 3. Finde Input und Button innerhalb der Produktkarte
        quantity_input = product_card.find_element(*self.QUANTITY_INPUT)
        add_button = product_card.find_element(*self.ADD_TO_CART_BUTTON)

        # 4. Setze Menge und klicke
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        add_button.click()

    # Pagination helpers
    def has_next_page(self) -> bool:
        """
        Prüft, ob eine nächste Seite verfügbar ist.
        Nutzt find_elements, um Exception zu vermeiden.
        """
        buttons = self.find_elements_no_wait(self.NEXT_PAGE_BUTTON)
        if not buttons:
            return False

        # Prüfe ob Button disabled ist
        button_classes = buttons[0].get_attribute("class")
        return "disabled" not in button_classes

    def go_to_next_page(self):
        """Navigiert zur nächsten Seite und wartet auf Produktkarten"""
        self.click(self.NEXT_PAGE_BUTTON)
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_CARD))

    # Compliance / Security
    def is_underage_notice_visible(self) -> bool:
        """Prüft, ob die Minderjährigen-Warnung angezeigt wird"""
        elements = self.find_elements_no_wait(self.UNDERAGE_NOTICE)
        if not elements:
            return False
        return elements[0].is_displayed()