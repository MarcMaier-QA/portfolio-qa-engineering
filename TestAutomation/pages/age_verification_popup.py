from selenium.webdriver.common.by import By
from TestAutomation.pages.base_page import BasePage


class AgeVerificationPopup(BasePage):
    """
    Page Object representing the age verification popup.

    This popup is displayed when a user accesses the shop
    and must confirm that they are at least 18 years old
    in order to view or purchase age-restricted products
    (e.g. alcoholic beverages).
    """

    # Locators
    POPUP_CONTAINER = (By.CSS_SELECTOR, "input[placeholder='DD-MM-YYYY']")
    DATE_INPUT = (By.XPATH, "//input[@placeholder='DD-MM-YYYY']")
    CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space()='Confirm']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(text(),'You are of age')]")
    WARNING_MESSAGE = (By.XPATH, "//div[contains(text(),'You are underage')]")

    # State checks
    def is_popup_displayed(self) -> bool:
        """
        Checks whether the age verification popup is displayed.

        Uses a short explicit wait to determine if the popup
        container becomes visible.
        """
        return self.is_visible(self.POPUP_CONTAINER)

    def is_date_input_visible(self) -> bool:
        """
        Checks if the date input field is visible.

        This is used as an alternative popup detection mechanism
        in case the popup container itself is not reliable.
        """
        elements = self.find_elements_no_wait(self.DATE_INPUT)
        if not elements:
            return False
        return elements[0].is_displayed()

    def is_success_message_displayed(self) -> bool:
        """
        Checks if the success message is displayed.

        The success message appears when the user enters
        a birthdate indicating they are 18 years or older.
        """
        elements = self.find_elements_no_wait(self.SUCCESS_MESSAGE)
        if not elements:
            return False
        return elements[0].is_displayed()

    def is_warning_message_displayed(self) -> bool:
        """
        Checks if the warning message is displayed.

        The warning message appears when the user enters
        a birthdate indicating they are under 18 years old.
        """
        elements = self.find_elements_no_wait(self.WARNING_MESSAGE)
        if not elements:
            return False
        return elements[0].is_displayed()

    def get_success_message_text(self) -> str:
        """
        Returns the text of the success message.

        If the message is not present, an empty string is returned
        to avoid unnecessary exceptions in tests.
        """
        elements = self.find_elements_no_wait(self.SUCCESS_MESSAGE)
        if not elements:
            return ""
        return elements[0].text

    def get_warning_message_text(self) -> str:
        """
        Returns the text of the warning message.

        If the message is not present, an empty string is returned
        to allow safe assertions in test cases.
        """
        elements = self.find_elements_no_wait(self.WARNING_MESSAGE)
        if not elements:
            return ""
        return elements[0].text

    # Actions
    def enter_birthdate(self, birthdate: str):
        """
        Enters a birthdate into the date input field.

        Args:
            birthdate: Birthdate in format DD-MM-YYYY
                       (e.g. "27-08-2007")
        """
        self.type(self.DATE_INPUT, birthdate)

    def click_confirm(self):
        """
        Clicks the confirm button to submit the entered birthdate.
        """
        self.click(self.CONFIRM_BUTTON)

    def submit_birthdate(self, birthdate: str):
        """
        Performs the complete interaction for age verification:
        entering a birthdate and confirming it.

        Args:
            birthdate: Birthdate in format DD-MM-YYYY
        """
        self.enter_birthdate(birthdate)
        self.click_confirm()

    def confirm_age(self, birthdate: str = "27-08-2007"):
        """
        Convenience method to confirm age verification.

        This method is primarily used in fixtures or setup steps
        to ensure the popup is handled before test execution.

        Args:
            birthdate: A valid birthdate indicating an adult user.
                       Defaults to "27-08-2007".
        """
        # Check whether the popup is present at all
        if not self.is_popup_displayed() and not self.is_date_input_visible():
            return  # Popup not shown → nothing to do

        self.submit_birthdate(birthdate)

        # Wait until the popup disappears or a message is shown
        self.wait_until_not_visible(self.POPUP_CONTAINER)
