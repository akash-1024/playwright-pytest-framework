import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from pages.locators.cart_locators import CartLocators


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def item_count(self) -> int:
        return self.page.locator(CartLocators.CART_ITEM).count()

    @allure.step("Remove product {product_id} from the cart")
    def remove_item(self, product_id: str) -> None:
        self.page.locator(CartLocators.remove_button(product_id)).click()

    @allure.step("Start checkout")
    def start_checkout(self) -> CheckoutPage:
        self.page.locator(CartLocators.CHECKOUT_BUTTON).click()
        return CheckoutPage(self.page)
