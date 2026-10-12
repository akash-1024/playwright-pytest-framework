import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.locators.checkout_locators import CheckoutLocators


class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @allure.step("Enter checkout information")
    def enter_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.page.locator(CheckoutLocators.FIRST_NAME).fill(first_name)
        self.page.locator(CheckoutLocators.LAST_NAME).fill(last_name)
        self.page.locator(CheckoutLocators.POSTAL_CODE).fill(postal_code)
        self.page.locator(CheckoutLocators.CONTINUE_BUTTON).click()

    @allure.step("Finish the order")
    def finish_order(self) -> str:
        self.page.locator(CheckoutLocators.FINISH_BUTTON).click()
        return self.page.locator(CheckoutLocators.COMPLETE_HEADER).inner_text()
