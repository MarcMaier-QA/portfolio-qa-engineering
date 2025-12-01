from selenium.webdriver.support.ui import Select


class Actions:
    def __init__(self, driver, waiter):
        self.driver = driver
        self.wait = waiter

    def click(self, locator):
        self.wait.clickable(locator).click()

    def type(self, locator, text):
        self.wait.visible(locator).send_keys(text)

    def select_value(self, locator, value):
        select = Select(self.wait.visible(locator))
        select.select_by_value(value)

    def select_text(self, locator, text):
        select = Select(self.wait.visible(locator))
        select.select_by_visible_text(text)
