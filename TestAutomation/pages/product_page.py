from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TestAutomation.pages.base_page import BasePage


class ProductPage(BasePage):

    # Page Load
    PRODUCT_TITLE = (By.TAG_NAME, "h2")

    # Rating Form
    RATING_FORM = (By.XPATH, "//div[contains(@class,'interactive-rating')]")
    RATING_STAR = lambda self, n: (
        By.XPATH,
        f"//div[contains(@class,'interactive-rating')]/span[{n}]"
    )
    COMMENT_TEXTAREA = (By.XPATH, "//textarea[contains(@class,'new-review-form-control')]")
    SEND_BUTTON = (By.XPATH, "//button[contains(.,'Send')]")
    RATING_ERROR = (By.XPATH, "//div[contains(text(),'Invalid input for the field')]")

    # Review / Delete
    REVIEW_MENU_BUTTON = (By.CSS_SELECTOR, ".comment .menu-icon")
    DROPDOWN_MENU = (By.CSS_SELECTOR, ".dropdown-menu")
    DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Delete']")
    ADD_COMMENT_HEADER = (By.XPATH, "//h5[contains(text(),'Add a comment')]")

    # Navigation
    def navigate_to(self, url: str):
        self.open(url)
        self.wait.until(EC.visibility_of_element_located(self.PRODUCT_TITLE))
        return self

    def scroll_to(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

    def wait_for_user_review(self, username: str):
        locator = self.user_review_container(username)
        self.wait.until(EC.visibility_of_element_located(locator))
        self.scroll_to(locator)
        return self

    # Review Locators
    def user_review_container(self, username: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'comment')]"
            f"[.//strong[normalize-space()='{username}']]"
        )

    def user_review_text(self, username: str):
        return (
            By.XPATH,
            f"{self.user_review_container(username)[1]}//p"
        )

    def user_review_rating(self, username: str):
        return (
            By.XPATH,
            f"{self.user_review_container(username)[1]}//span[contains(@class,'small')]"
        )

    # Assertions / Getters
    def is_rating_form_visible(self) -> bool:
        elements = self.find_elements_no_wait(self.RATING_FORM)
        return bool(elements and elements[0].is_displayed())

    def is_comment_visible(self, username: str, comment_text: str) -> bool:
        """
        Prüft bewusst OHNE Wait, ob ein Kommentartext vorhanden ist.
        Liefert False bei leerem <p> (bekannter Bug).
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
        Gibt die Sternebewertung des angegebenen Users zurück.
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
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        return bool(elements and elements[0].is_displayed())

    def get_rating_error_text(self) -> str:
        elements = self.find_elements_no_wait(self.RATING_ERROR)
        return elements[0].text if elements else ""

    # Actions
    def click_rating_star(self, stars: int):
        if stars > 0:
            self.click(self.RATING_STAR(stars))
        return self

    def enter_comment(self, comment: str):
        self.type(self.COMMENT_TEXTAREA, comment)
        return self

    def submit_rating(self):
        self.click(self.SEND_BUTTON)
        return self

    def rate_product(self, stars: int = 0, comment: str = ""):
        if stars > 0:
            self.click_rating_star(stars)

        if comment:
            self.enter_comment(comment)

        self.submit_rating()

        if stars == 0:
            self.wait.until(EC.visibility_of_element_located(self.RATING_ERROR))
            return self.get_rating_error_text()

        if self.is_rating_error_visible():
            return self.get_rating_error_text()

        return self

    def delete_my_review(self):
        # 1. Existiert überhaupt ein Review?
        elements = self.find_elements_no_wait(self.REVIEW_MENU_BUTTON)
        if not elements:
            return self

        # 2. Scroll zum Review-Menü
        self.scroll_to(self.REVIEW_MENU_BUTTON)

        # 3. Jetzt auf Klickbarkeit warten
        self.wait.until(
            EC.element_to_be_clickable(self.REVIEW_MENU_BUTTON)
        ).click()

        # 4. Dropdown erscheint
        self.wait.until(
            EC.visibility_of_element_located(self.DROPDOWN_MENU)
        )

        # 5. Delete klicken
        self.wait.until(
            EC.element_to_be_clickable(self.DELETE_BUTTON)
        ).click()

        # 6. Alert bestätigen
        self.driver.switch_to.alert.accept()

        # 7. Warten bis wieder „Add a comment“-State erreicht ist
        self.wait.until(
            EC.visibility_of_element_located(self.ADD_COMMENT_HEADER)
        )

        self.wait.until(
            EC.invisibility_of_element_located(self.REVIEW_MENU_BUTTON)
        )

        return self
