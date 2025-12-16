from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage


class ProductPage(BasePage):

    # Locators
    PRODUCT_TITLE = (By.TAG_NAME, "h2")

    # Rating
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

    # Navigation
    def wait_until_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))

    # Assertions helpers
    def is_product_name_displayed(self, expected_name: str) -> bool:
        title = self.get_text(self.PRODUCT_TITLE)
        return title.strip() == expected_name

    def is_rating_error_visible(self) -> bool:
        return self.is_visible(self.RATING_ERROR)

    def get_displayed_rating(self) -> int:
        text = self.get_text(self.DISPLAYED_RATING)
        return int(text) if text.isdigit() else 0

    # Actions
    def click_rating_star(self, stars: int):
        self.click(self.RATING_STAR(stars))

    def enter_comment(self, comment: str):
        self.type(self.COMMENT_TEXTAREA, comment)

    def submit_rating(self):
        self.click(self.SEND_BUTTON)
