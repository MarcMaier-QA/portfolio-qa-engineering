from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Aufgabe 1 (Web-Automatisierung mit Selenium)
# Testdaten (User Credentials)
user_name = "standard_user"
user_password = "secret_sauce"

# Setup: Browser öffnen
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")

# Login: Eingabefelder und Login-Button finden
username_field = driver.find_element(By.ID, "user-name")
password_field = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")

# Login ausführen
username_field.send_keys(user_name)
password_field.send_keys(user_password)
login_button.click()

# Warten, um den erfolgreichen Login und die Produktseite zu sehen
time.sleep(3)

# Verification: Prüfen, ob Login erfolgreich war (Products-Titel sichtbar)
title_element = driver.find_element(By.CLASS_NAME, "title")
assert title_element.text == "Products"

# Verification: Prüfen, ob das Produkt "Sauce Labs Backpack" angezeigt wird
product = driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
assert product.text == "Sauce Labs Backpack"

# Beendet die session
driver.quit()
