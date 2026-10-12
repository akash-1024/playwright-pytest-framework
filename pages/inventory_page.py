import allure
from playwright.sync_api import Page

from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.locators.inventory_locators import InventoryLocators


class InventoryPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def item_count(self) -> int:
        return self.page.locator(InventoryLocators.INVENTORY_ITEM).count()

    @allure.step("Add product {product_id} to the cart")
    def add_to_cart(self, product_id: str) -> None:
        self.page.locator(InventoryLocators.add_to_cart_button(product_id)).click()

    @allure.step("Open the shopping cart")
    def open_cart(self) -> CartPage:
        self.page.locator(InventoryLocators.CART_LINK).click()
        return CartPage(self.page)
