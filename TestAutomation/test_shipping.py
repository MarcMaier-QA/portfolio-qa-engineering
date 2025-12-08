import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_cart_if_not_empty(driver):
    """
    Leert den Warenkorb zuverlässig per Klick auf den Remove-Button.
    """
    CHECKOUT = "https://grocerymate.masterschool.com/checkout"
    driver.get(CHECKOUT)
    wait = WebDriverWait(driver, 10)

    while True:
        # Alle Entfernen-Buttons im Warenkorb finden
        remove_buttons = driver.find_elements(By.XPATH, "/html/body/div[1]/div/section/div/div[1]/div/div[1]/div/div/div[1]/a")

        if not remove_buttons:
            break  # Warenkorb ist leer

        for btn in remove_buttons:
            try:
                wait.until(EC.element_to_be_clickable(btn))
                driver.execute_script("arguments[0].click();", btn)
                # kurz warten, bis das Element aus dem DOM entfernt wurde
                time.sleep(0.3)
            except:
                continue

        # Nach jeder Runde kurz warten, bis DOM aktualisiert ist
        time.sleep(0.5)

    # Seite neu laden, um sicherzugehen
    driver.get(CHECKOUT)
    time.sleep(1)



def find_product_card(driver, product_name, timeout=10):
    """Findet ein Produkt auf allen Shop-Seiten (inkl. Pagination)."""
    wait = WebDriverWait(driver, timeout)

    while True:
        cards = driver.find_elements(
            By.XPATH, f"//p[@class='lead' and text()='{product_name}']/ancestor::div[contains(@class,'product-card')]"
        )
        if cards:
            return cards[0]

        next_buttons = driver.find_elements(By.XPATH, "//button[contains(@class,'pagination-link') and text()='Next']")
        if not next_buttons or "disabled" in next_buttons[0].get_attribute("class"):
            break

        next_buttons[0].click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'product-card')]")))
        time.sleep(0.3)

    raise Exception(f"Product '{product_name}' not found in any page")


def confirm_age_popup(driver):
    """Bestätigt das Age-Popup, falls es erscheint."""
    try:
        date_input = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='DD-MM-YYYY']"))
        )
        date_input.clear()
        date_input.send_keys("27-08-2007")
        driver.find_element(By.XPATH, "//button[text()='Confirm']").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'product-card')]"))
        )
        time.sleep(1)
    except:
        pass


@pytest.mark.parametrize(
    "product_name, quantity, expected_shipping, expected_product_total, expected_total",
    [
        ("Cherries", 10, "0€", "25.00€", "25.00€"),
        ("Cherries", 2, "5€", "5.00€", "10.00€")
    ]
)
def test_shipping_cost(login, product_name, quantity, expected_shipping, expected_product_total, expected_total):
    CHECKOUT = "https://grocerymate.masterschool.com/checkout"
    SHOP = "https://grocerymate.masterschool.com/store"
    driver = login

    # 1. Warenkorb leeren
    clear_cart_if_not_empty(driver)

    # 2. Shop öffnen
    driver.get(SHOP)

    # 3. Age-Popup bestätigen
    confirm_age_popup(driver)

    # 4. Produkt suchen
    product_card = find_product_card(driver, product_name)
    qty_input = product_card.find_element(By.XPATH, ".//input[@type='number']")
    add_btn = product_card.find_element(By.XPATH, ".//button[contains(@class,'btn-cart')]")

    # 5. Menge setzen wie ein Nutzer
    qty_input.clear()
    time.sleep(0.2)
    for digit in str(quantity):
        qty_input.send_keys(digit)
        time.sleep(0.1)

    add_btn.click()
    time.sleep(1)

    # Sicherstellen, dass die Menge übernommen wurde
    current_qty = int(qty_input.get_attribute("value"))
    if current_qty != quantity:
        qty_input.clear()
        for digit in str(quantity):
            qty_input.send_keys(digit)
            time.sleep(0.1)
        add_btn.click()
        time.sleep(1)

    # Checkout öffnen und Werte prüfen
    driver.get(CHECKOUT)
    wait = WebDriverWait(driver, 15)

    shipping_cost = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='shipment-container']/h5[2]"))
    ).text
    product_total = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='product-total-container']/h5[2]"))
    ).text
    total = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='total-container']/h5[2]"))
    ).text

    # 7. Assertions
    assert shipping_cost == expected_shipping
    assert product_total == expected_product_total
    assert total == expected_total
