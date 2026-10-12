import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from pages.locators.login_locators import LoginLocators


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step("Log in as {username}")
    def login(self, username: str, password: str) -> InventoryPage:
        self.page.locator(LoginLocators.USERNAME).fill(username)
        self.page.locator(LoginLocators.PASSWORD).fill(password)
        self.page.locator(LoginLocators.LOGIN_BUTTON).click()
        return InventoryPage(self.page)

    def error_message(self) -> str:
        return self.page.locator(LoginLocators.ERROR_MESSAGE).inner_text()
