from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage


class ProductPage(BasePage):

    # Page load identifier
    # The product title is used as a stable indicator that the page is fully loaded
    PRODUCT_TITLE = (By.TAG_NAME, "h2")

    # Rating form elements
    RATING_FORM = (By.XPATH, "//div[contains(@class,'interactive-rating')]")

    # Dynamic locator for rating stars
    # Using a lambda keeps the locator flexible while staying readable
    RATING_STAR = lambda self, n: (
        By.XPATH,
        f"//div[contains(@class,'interactive-rating')]/span[{n}]"
    )

    COMMENT_TEXTAREA = (By.XPATH, "//textarea[contains(@class,'new-review-form-control')]")
    SEND_BUTTON = (By.XPATH, "//button[contains(.,'Send')]")
    RATING_ERROR = (By.XPATH, "//div[contains(text(),'Invalid input for the field')]")

    # Review / delete elements
    REVIEW_MENU_BUTTON = (By.CSS_SELECTOR, ".comment .menu-icon")
    DROPDOWN_MENU = (By.CSS_SELECTOR, ".dropdown-menu")
    DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Delete']")
    ADD_COMMENT_HEADER = (By.XPATH, "//h5[contains(text(),'Add a comment')]")

    def wait_until_loaded(self):
        """
        Waits until the product page is fully loaded.

        The product title is used instead of URL checks,
        as it reflects the actual user-visible state.
        """
        self.wait.until(
            EC.visibility_of_element_located(self.PRODUCT_TITLE),
            message="ProductPage: product title not visible"
        )
        return self

    # Navigation helpers
    def scroll_to(self, locator):
        """
        Scrolls the given element into view.

        This is required for elements that are present in the DOM
        but not interactable until visible (e.g. review actions).
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    def wait_for_user_review(self, username: str):
        """
        Waits until the review of the given user becomes visible
        and scrolls to it for further interaction.
        """
        locator = self.user_review_container(username)
        self.wait.until(EC.visibility_of_element_located(locator))
        self.scroll_to(locator)
        return self

    # Review-related locators
    def user_review_container(self, username: str):
        """
        Returns the container element for a specific user's review.
        """
        return (
            By.XPATH,
            f"//div[contains(@class,'comment')]"
            f"[.//strong[normalize-space()='{username}']]"
        )

    def user_review_rating(self, username: str):
        """
        Returns the locator for the rating value of a user's review.
        """
        return (
            By.XPATH,
            f"{self.user_review_container(username)[1]}//span[contains(@class,'small')]"
        )

    # State checks
    def is_rating_form_visible(self) -> bool:
        """
        Checks whether the rating form is currently visible.

        Uses a no-wait lookup to allow flexible state assertions.
        """
        elements = self.find_elements_no_wait(self.RATING_FORM)
        return bool(elements and elements[0].is_displayed())

    def is_comment_visible(self, username: str, comment_text: str) -> bool:
        """
        Intentionally checks WITHOUT an explicit wait.

        Returns False if the <p> element is empty,
        which reflects a known application bug.
        """
        locator = (
            By.XPATH,
            f"//div[contains(@class,'comment')]"
            f"[.//strong[normalize-space()='{username}']]"
            f"//p[normalize-space()='{comment_text}']"
        )

        elements = self.find_elements_no_wait(locator)
        return bool(elements and elements[0].is_displayed())

    def get_displayed_rating(self, username: str) -> int:
        """
        Returns the displayed star rating for the given user.
        """
        rating_locator = (
            By.XPATH,
            f"//div[contains(@class,'comment')]"
            f"[.//strong[normalize-space()='{username}']]"
            f"//span[@class='small']"
        )

        self.wait.until(EC.visibility_of_element_located(rating_locator))

        text = self.get_text(rating_locator)
        return int(text.strip("()"))

    def is_rating_error_visible(self) -> bool:
        """
        Checks whether a rating validation error is visible.
        """
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        return bool(elements and elements[0].is_displayed())

    def get_rating_error_text(self) -> str:
        """
        Returns the rating error message text if present.
        """
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        return elements[0].text if elements else ""

    # Actions
    def click_rating_star(self, stars: int):
        """
        Clicks the given star rating if a valid value is provided.
        """
        if stars > 0:
            self.click(self.RATING_STAR(stars))
        return self

    def enter_comment(self, comment: str):
        """
        Enters a review comment into the textarea.
        """
        self.type(self.COMMENT_TEXTAREA, comment)
        return self

    def submit_rating(self):
        """
        Submits the rating form.
        """
        self.click(self.SEND_BUTTON)
        return self

    def rate_product(self, stars: int = 0, comment: str = ""):
        """
        Rates a product with optional stars and comment.

        Handles both valid submissions and expected validation errors.
        """
        if stars > 0:
            self.click_rating_star(stars)

        if comment:
            self.enter_comment(comment)

        self.submit_rating()

        # Special case: submitting without stars is expected to fail
        if stars == 0:
            self.wait.until(EC.visibility_of_element_located(self.RATING_ERROR))
            return self.get_rating_error_text()

        if self.is_rating_error_visible():
            return self.get_rating_error_text()

        return self

    def delete_my_review(self):
        """
        Deletes the currently logged-in user's review if it exists.

        The method safely exits if no review is present.
        """
        # 1. Check if a review exists at all
        elements = self.find_elements_no_wait(self.REVIEW_MENU_BUTTON)
        if not elements:
            return self

        # 2. Scroll to the review menu to ensure visibility
        self.scroll_to(self.REVIEW_MENU_BUTTON)

        # 3. Wait until the menu is clickable
        self.wait.until(
            EC.element_to_be_clickable(self.REVIEW_MENU_BUTTON)
        ).click()

        # 4. Wait for dropdown to appear
        self.wait.until(
            EC.visibility_of_element_located(self.DROPDOWN_MENU)
        )

        # 5. Click delete
        self.wait.until(
            EC.element_to_be_clickable(self.DELETE_BUTTON)
        ).click()

        # 6. Confirm browser alert
        self.driver.switch_to.alert.accept()

        # 7. Wait until the page returns to the "Add a comment" state
        self.wait.until(
            EC.visibility_of_element_located(self.ADD_COMMENT_HEADER)
        )

        self.wait.until(
            EC.invisibility_of_element_located(self.REVIEW_MENU_BUTTON)
        )

        return self
