import allure
import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from pages.locators.inventory_locators import InventoryLocators
from pages.login_page import LoginPage


@pytest.mark.smoke
@allure.title("Standard user can log in")
def test_standard_user_can_log_in(logged_in_inventory_page, page: Page) -> None:
    expect(page).to_have_url(f"{settings.base_url}/inventory.html")
    expect(page.locator(InventoryLocators.TITLE)).to_have_text("Products")
    expect(page.locator(InventoryLocators.INVENTORY_ITEM)).to_have_count(6)


@allure.title("Invalid credentials show an error")
def test_invalid_credentials_show_error(login_page: LoginPage) -> None:
    login_page.login("invalid_user", "wrong_password")
    assert "Username and password do not match" in login_page.error_message()
