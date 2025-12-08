import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Helper-Funktionen
def go_to_product(driver, product_url):
    driver.get(product_url)


def rate_stars(driver, stars=0):
    star_5 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'rating-stars')]/span[5]")
        )
    )
    star_5.click()


def write_comment(driver, comment_text=""):
    if comment_text:
        comment_box = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='What is your view?']"))
        )
        comment_box.send_keys(comment_text)


def submit(driver):
    send_btn = driver.find_element(By.XPATH, "//button[contains(.,'Send')]")
    send_btn.click()


def verify_comment(driver, author, comment_text):
    comments = driver.find_elements(By.XPATH, "//div[@class='comment-body']")
    found = False
    for c in comments:
        author_elem = c.find_element(By.TAG_NAME, "strong")
        text_elem = c.find_element(By.TAG_NAME, "p")
        if author_elem.text == author and text_elem.text == comment_text:
            found = True
            break
    assert found, f"Kommentar von '{author}' mit Text '{comment_text}' wurde nicht gefunden"


def verify_rating(driver, expected_stars):
    rating_span = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[@class='small']")
        )
    )
    stars_text = rating_span.text.strip()   # Beispiel: "(4)"
    stars_number = int(stars_text.replace("(", "").replace(")", ""))

    assert stars_number == expected_stars, \
        f"Erwartet: {expected_stars} Sterne, angezeigt: {stars_number}"


def buy_product(driver):
    pass


#-----------------------------------------------------------------------------------------------------------------------



# Tests
def test_5_stars_with_comment(login):
    driver = login
    product_url = "https://grocerymate.masterschool.com/product/66b3a57b3fd5048eacb4798f"  # Oranges
# todo:
    # <- heir die kaufe produkt einfügen
    go_to_product(driver, product_url)

    # Prüfen, ob Kommentarfeld sichtbar ist
    try:
        comment_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//textarea[@placeholder='What is your view?']")
            )
        )
    except TimeoutException:
        pytest.skip("Kommentarfeld nicht sichtbar. Produkt vermutlich nicht gekauft.")

    rate_stars(driver, 5)
    write_comment(driver, "Tolles Produkt!")
    submit(driver)

    verify_comment(driver, author="Testi Mc_tester", comment_text="Tolles Produkt!")


def test_4_stars_without_comment(login):
    driver = login
    product_url = "https://grocerymate.masterschool.com/product/66b3a57b3fd5048eacb47990"

    go_to_product(driver, product_url)

    # Prüfen, ob Nutzer kommentieren darf, suchen das Kommentar-Feld
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//textarea[@placeholder='What is your view?']")
            )
        )
    except TimeoutException:
        pytest.skip("Kommentarfeld nicht sichtbar. Produkt vermutlich nicht gekauft.")

    # Nur Sterne setzen
    rate_stars(driver, 4)
    submit(driver)

    # Sterne überprüfen anhand der Anzeige (4)
    verify_rating(driver, expected_stars=4)

