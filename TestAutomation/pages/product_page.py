from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from TestAutomation.utils.constants import DEFAULT_WAIT_TIME, TEST_USER_NAME


class ProductPage:
    def __init__(self, driver):
        self.driver = driver

        # Locators
        self.RATING_STAR = lambda n: (By.XPATH, f"//div[contains(@class,'rating-stars')]/span[{n}]")
        self.COMMENT_TEXTAREA = (By.XPATH, "//textarea[@placeholder='What is your view?']")
        self.SEND_BUTTON = (By.XPATH, "//button[contains(.,'Send')]")
        self.COMMENT_BODY = (By.XPATH, "//div[@class='comment-body']")
        self.DISPLAYED_RATING = (By.XPATH, "//span[@class='small']")
        self.RATING_INPUT_FORM = (By.XPATH, "//div[contains(@class, 'rating-stars')]")

    def navigate_to(self, product_url: str):
        """Navigiert direkt zur Produktseite und wartet auf das Formular."""
        self.driver.get(product_url)
        # Expliziter Wait, um sicherzustellen, dass die Seite geladen ist
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.RATING_INPUT_FORM)
        )

    def rate_product(self, stars: int, comment: str = None):
        """
        Kombiniert Aktion:
            Sterne setzen und optionalen Kommentar schreiben.
        """
        # 1. Sterne anklicken
        star_locator = self.RATING_STAR(stars)
        WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(star_locator)
        ).click()

        # 2. Kommentar schreiben
        if comment:
            comment_box = self.driver.find_element(*self.COMMENT_TEXTAREA)
            comment_box.send_keys(comment)

        # 3. Absenden
        self.driver.find_element(*self.SEND_BUTTON).click()

    def is_comment_visible(self, author: str = TEST_USER_NAME, comment_text: str = "" ):
        """Prüft, ob ein spezifischer Kommentar sichtbar ist"""

        # 1. Warten, bis mindestens EINE Kommentar-Box existiert (presence_of_all_elements_located)
        try:
            WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
                EC.presence_of_element_located(self.COMMENT_BODY)
            )
        except TimeoutException:
            # Wenn nach der Wartezeit keine Kommentare existieren, gehen wir weiter und finden 0 Elemente.
            pass

        # 2. Alle Kommentar-Elemente suchen (find_elements)
        comments = self.driver.find_elements(*self.COMMENT_BODY)
        for c in comments:
            try:
                # Suche relativ zur gefundenen Kommentar-Box
                author_element = c.find_element(By.TAG_NAME, "strong")
                text_element = c.find_element(By.TAG_NAME, "p")
                if author_element.text == author and text_element.text == comment_text:
                    return True # Kommentar gefunden!
            except NoSuchElementException:
                # Wir ignorieren Kommentare, die nicht die erwartete innere Struktur haben.
                continue

        return False # Kommentar nicht gefunden!

    def get_displayed_rating(self) -> int:
        """Gibt die aktuell angezeigte Sterne-Anzahl zurück"""
        rating_span = WebDriverWait(self.driver, DEFAULT_WAIT_TIME).until(
            EC.visibility_of_element_located(self.DISPLAYED_RATING)
        )
        stars_text = rating_span.text.strip()
        return int(stars_text.replace("(", "").replace(")", ""))
