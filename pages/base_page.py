from playwright.sync_api import Page

from config.settings import settings


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, path: str = "/") -> None:
        self.page.goto(f"{settings.base_url}{path}")
