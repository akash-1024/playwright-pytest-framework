from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

from config.settings import settings
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture(scope="session")
def browser(
    playwright: Playwright,
    request: pytest.FixtureRequest,
) -> Generator[Browser, None, None]:
    browser_types = {
        "chromium": playwright.chromium,
        "firefox": playwright.firefox,
        "webkit": playwright.webkit,
    }
    if settings.browser not in browser_types:
        supported = ", ".join(browser_types)
        raise ValueError(f"Unsupported PLAYWRIGHT_BROWSER '{settings.browser}'. Choose: {supported}.")

    headed = request.config.getoption("headed", default=True)
    launched_browser = browser_types[settings.browser].launch(
        headless=settings.headless and not headed
    )
    yield launched_browser
    launched_browser.close()


@pytest.fixture
def page(browser: Browser, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    context: BrowserContext = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.set_default_timeout(settings.timeout_ms)
    yield page

    try:
        report = getattr(request.node, "rep_call", None)
        if report is not None and report.failed:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
    finally:
        context.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture
def logged_in_inventory_page(login_page: LoginPage) -> InventoryPage:
    return login_page.login(settings.username, settings.password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())
