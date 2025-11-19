import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

VALID_PASSWORD = "secret_sauce"
USERS = [
    ("standard_user"),
    ("locked_out_user"),
    ("problem_user"),
    ("performance_glitch_user"),
    ("error_user"),
    ("visual_user"),
]

@pytest.fixture
def driver():
    chrome_driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()