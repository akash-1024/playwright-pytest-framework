import allure
import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.inventory_page import InventoryPage
from pages.locators.cart_locators import CartLocators
from pages.locators.checkout_locators import CheckoutLocators


@pytest.mark.smoke
@allure.title("User can add and remove a product")
def test_add_and_remove_product_from_cart(logged_in_inventory_page: InventoryPage, page: Page) -> None:
    logged_in_inventory_page.add_to_cart("sauce-labs-backpack")
    cart_page = logged_in_inventory_page.open_cart()

    expect(page.locator(CartLocators.CART_ITEM)).to_have_count(1)
    cart_page.remove_item("sauce-labs-backpack")
    expect(page.locator(CartLocators.CART_ITEM)).to_have_count(0)


@pytest.mark.smoke
@allure.title("User can complete checkout")
def test_user_can_complete_checkout(logged_in_inventory_page: InventoryPage, page: Page) -> None:
    logged_in_inventory_page.add_to_cart("sauce-labs-backpack")
    checkout_page = logged_in_inventory_page.open_cart().start_checkout()
    checkout_page.enter_information("Ada", "Lovelace", "12345")

    expect(page).to_have_url(f"{settings.base_url}/checkout-step-two.html")
    assert checkout_page.finish_order() == "Thank you for your order!"
    expect(page.locator(CheckoutLocators.COMPLETE_HEADER)).to_be_visible()
