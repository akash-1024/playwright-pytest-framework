"""Load SauceDemo and browser settings from the environment or a local .env file."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com").rstrip("/")
    username: str = os.getenv("SAUCEDEMO_USERNAME", "standard_user")
    password: str = os.getenv("SAUCEDEMO_PASSWORD", "secret_sauce")
    browser: str = os.getenv("PLAYWRIGHT_BROWSER", "chromium").lower()
    headless: bool = _get_bool("PLAYWRIGHT_HEADLESS", True)
    timeout_ms: int = int(os.getenv("PLAYWRIGHT_TIMEOUT_MS", "10000"))


settings = Settings()
