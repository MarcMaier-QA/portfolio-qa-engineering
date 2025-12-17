from selenium.webdriver.common.by import By
from TestAutomation.pages.base_page import BasePage


class AgeVerificationPopup(BasePage):
    """
    Page Object für das Altersverifikations-Popup.

    Wird angezeigt, wenn Nutzer auf alkoholische Produkte zugreifen.
    """

    # Locators
    POPUP_CONTAINER = (By.CSS_SELECTOR, "input[placeholder='DD-MM-YYYY']")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(),'You are of age')]")
    WARNING_MESSAGE = (By.XPATH, "//div[contains(text(),'You are underage')]")

    # State checks
    def is_popup_displayed(self) -> bool:
        """Prüft mit kurzem Wait, ob das Popup erscheint."""
        return self.is_visible(self.POPUP_CONTAINER)

    def is_date_input_visible(self) -> bool:
        """
        Prüft, ob das Datumseingabefeld sichtbar ist.
        Alternative Methode zur Popup-Erkennung.
        """
        elements = self.find_elements_no_wait(self.DATE_INPUT)
        if not elements:
            return False
        return elements[0].is_displayed()

    def is_success_message_displayed(self) -> bool:
        """
        Prüft, ob die Erfolgsmeldung angezeigt wird.
        (Erscheint, wenn User über 18 ist)
        """
        elements = self.find_elements_no_wait(self.SUCCESS_MESSAGE)
        if not elements:
            return False
        return elements[0].is_displayed()

    def is_warning_message_displayed(self) -> bool:
        """
        Prüft, ob die Warnmeldung angezeigt wird.
        (Erscheint, wenn User unter 18 ist)
        """
        elements = self.find_elements_no_wait(self.WARNING_MESSAGE)
        if not elements:
            return False
        return elements[0].is_displayed()

    def get_success_message_text(self) -> str:
        """Gibt den Text der Erfolgsmeldung zurück"""
        elements = self.find_elements_no_wait(self.SUCCESS_MESSAGE)
        if not elements:
            return ""
        return elements[0].text

    def get_warning_message_text(self) -> str:
        """Gibt den Text der Warnmeldung zurück"""
        elements = self.find_elements_no_wait(self.WARNING_MESSAGE)
        if not elements:
            return ""
        return elements[0].text

    # Actions
    def enter_birthdate(self, birthdate: str):
        """
        Gibt ein Geburtsdatum ein (Format: DD-MM-YYYY).

        Args:
            birthdate: Geburtsdatum im Format DD-MM-YYYY (z.B. "27-08-2007")
        """
        self.type(self.DATE_INPUT, birthdate)

    def click_confirm(self):
        """Klickt den Confirm-Button"""
        self.click(self.CONFIRM_BUTTON)

    def submit_birthdate(self, birthdate: str):
        """
        Komplett-Aktion: Geburtsdatum eingeben und bestätigen.

        Args:
            birthdate: Geburtsdatum im Format DD-MM-YYYY
        """
        self.enter_birthdate(birthdate)
        self.click_confirm()

    def confirm_age(self, birthdate: str = "27-08-2007"):
        """
        Convenience-Methode: Bestätigt das Alter mit einem Standard-Geburtsdatum.
        Nützlich für Setup in Fixtures.

        Args:
            birthdate: Standard ist ein volljähriges Datum (27-08-2007)
        """
        # Prüfe ob Popup überhaupt da ist
        if not self.is_popup_displayed() and not self.is_date_input_visible():
            return  # Kein Popup, nichts zu tun

        self.submit_birthdate(birthdate)

        # Warte kurz bis Popup verschwindet oder Nachricht erscheint
        self.wait_until_not_visible(self.POPUP_CONTAINER)