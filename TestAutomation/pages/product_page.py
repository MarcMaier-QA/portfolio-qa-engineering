from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage


class ProductPage(BasePage):
    # Locators
    PRODUCT_TITLE = (By.TAG_NAME, "h2")

    # Rating Form
    RATING_FORM = (By.XPATH, "//div[contains(@class,'interactive-rating')]")
    RATING_STAR = lambda self, n: (
        By.XPATH,
        f"//div[contains(@class,'interactive-rating')]/span[{n}]"
    )
    COMMENT_TEXTAREA = (By.XPATH, "//textarea[contains(@class,'new-review-form-control')]")
    SEND_BUTTON = (By.XPATH, "//button[contains(.,'Send')]")

    # Feedback / Errors
    RATING_ERROR = (By.XPATH, "//div[contains(text(),'Invalid input for the field')]")

    # Displayed values
    DISPLAYED_RATING = (By.XPATH, "//span[@class='small']")

    # Comments section
    COMMENT_AUTHOR = lambda self, author: (
        By.XPATH,
        f"//div[contains(@class,'review')]//strong[contains(text(),'{author}')]"
    )
    COMMENT_TEXT = lambda self, text: (
        By.XPATH,
        f"//div[contains(@class,'review')]//p[contains(text(),'{text}')]"
    )

    # Review / Delete Locators
    ADD_COMMENT_HEADER = (By.XPATH, "//h5[contains(text(),'Add a comment')]")
    REVIEW_CONTAINER = (By.CSS_SELECTOR, ".comment")
    REVIEW_MENU_BUTTON = (By.CSS_SELECTOR, ".comment .menu-icon")
    DROPDOWN_MENU = (By.CSS_SELECTOR, ".dropdown-menu")
    DELETE_BUTTON = (By.XPATH,"//div[contains(@class, 'dropdown-menu')]//button[normalize-space()='Delete']")

    # Navigation
    def navigate_to(self, url: str):
        """Navigiert zu einer Produktseite"""
        self.open(url)
        self.wait_until_loaded()
        return self

    def wait_until_loaded(self):
        """Wartet bis die Produktseite vollständig geladen ist"""
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))

    # Rating Form Checks
    def is_rating_form_visible(self) -> bool:
        """
        Prüft, ob das Bewertungsformular sichtbar ist.
        Nutzt find_elements statt Exception.
        """
        elements = self.find_elements_no_wait(self.RATING_FORM)
        if not elements:
            return False
        return elements[0].is_displayed()

    # Assertions helpers
    def is_product_name_displayed(self, expected_name: str) -> bool:
        """Prüft ob der Produktname korrekt angezeigt wird"""
        title = self.get_text(self.PRODUCT_TITLE)
        return title.strip() == expected_name

    def is_rating_error_visible(self) -> bool:
        """Prüft ob die Rating-Fehlermeldung sichtbar ist"""
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        if not elements:
            return False
        return elements[0].is_displayed()

    def get_rating_error_text(self) -> str:
        """Gibt den Text der Fehlermeldung zurück (falls vorhanden)"""
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        if not elements:
            return ""
        return elements[0].text

    def get_displayed_rating(self) -> int:
        """Gibt die angezeigte Sternebewertung als Integer zurück"""
        text = self.get_text(self.DISPLAYED_RATING)

        # Klammern entfernen, falls vorhanden
        text = text.replace("(", "").replace(")", "")

        return int(text) if text.isdigit() else 0

    def is_comment_visible(self, author: str, comment_text: str) -> bool:
        """
        Prüft ob ein Kommentar mit bestimmtem Author und Text sichtbar ist.
        Nutzt find_elements um Exception zu vermeiden.
        """
        # Prüfe zuerst ob der Author existiert
        author_elements = self.find_elements_no_wait(self.COMMENT_AUTHOR(author))
        if not author_elements:
            return False

        # Prüfe dann ob der Kommentartext existiert
        text_elements = self.find_elements_no_wait(self.COMMENT_TEXT(comment_text))
        if not text_elements:
            return False

        return text_elements[0].is_displayed()

    # Actions
    def click_rating_star(self, stars: int):
        """Klickt auf einen bestimmten Stern (1-5)"""
        if stars > 0:
            self.click(self.RATING_STAR(stars))

    def enter_comment(self, comment: str):
        """Gibt einen Kommentar ein"""
        self.type(self.COMMENT_TEXTAREA, comment)

    def submit_rating(self):
        """Sendet die Bewertung ab"""
        self.click(self.SEND_BUTTON)

    def rate_product(self, stars: int = 0, comment: str = "") -> str:
        """
        Hauptmethode zum Bewerten eines Produkts.

        Args:
            stars: Anzahl der Sterne (0-5, 0 = keine Sterne)
            comment: Optionaler Kommentartext

        Returns:
            Fehlermeldung falls vorhanden, sonst leerer String
        """
        # 1. Sterne setzen (falls > 0)
        if stars > 0:
            self.click_rating_star(stars)

        # 2. Kommentar eingeben (falls vorhanden)
        if comment:
            self.enter_comment(comment)

        # 3. Absenden
        self.submit_rating()

        # 4. Prüfe auf Fehlermeldung
        if self.is_rating_error_visible():
            return self.get_rating_error_text()

        return ""

    def can_rate_product(self) -> bool:
        """
        Ein Produkt kann bewertet werden, wenn das Kommentar-Textfeld sichtbar ist.
        """
        elements = self.find_elements_no_wait(self.COMMENT_TEXTAREA)
        if not elements:
            return False
        return elements[0].is_displayed()

    def delete_my_review(self):
        """Löscht die eigene Bewertung, falls vorhanden."""
        # Wenn kein Review vorhanden → direkt zurück
        if not self.find_elements_no_wait(self.REVIEW_MENU_BUTTON):
            return self

        # Menü öffnen
        self.get_element(self.REVIEW_MENU_BUTTON).click()

        # Warten bis Dropdown sichtbar ist
        self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_MENU))

        # Delete drücken
        self.get_element(self.DELETE_BUTTON).click()

        # Bestätigungspopup akzeptieren
        self.driver.switch_to.alert.accept()

        # Warten bis Kommentar komplett weg ist
        self.wait.until(EC.visibility_of_element_located(self.ADD_COMMENT_HEADER))

        return self
