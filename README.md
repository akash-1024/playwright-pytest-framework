# SauceDemo UI Test Automation Framework

This repository contains an end-to-end UI test framework for the public
[SauceDemo](https://www.saucedemo.com/) shopping demo. It uses Python, pytest,
Playwright's synchronous API, the Page Object Model (POM), and Allure test
results.

The tests drive a real browser through the application and verify the login,
shopping cart, and checkout user flows. The default target and credentials in
`.env.example` are for the public demo site, not a production account.

## What the framework does

The current automated scenarios are:

| Test scenario | What it verifies |
| --- | --- |
| Successful login | A standard user reaches the Products inventory page and sees six products. |
| Rejected login | Invalid credentials show the expected login error. |
| Cart removal | A product can be added to the cart and then removed. |
| Checkout | A product can be checked out and the order confirmation is displayed. |

These tests are marked `smoke` where appropriate. They use pytest assertions
and Playwright's web-first assertions, which wait for the expected page state
instead of relying on fixed sleeps.

## Project structure

```text
config/
  settings.py                 Reads application and browser settings from .env
pages/
  base_page.py                Shared page behavior, including navigation
  login_page.py                Login actions and login error lookup
  inventory_page.py            Product selection and cart navigation
  cart_page.py                 Cart actions and checkout navigation
  checkout_page.py             Checkout form and order completion
  locators/
    login_locators.py           Login page selectors
    inventory_locators.py       Inventory page selectors
    cart_locators.py            Cart page selectors
    checkout_locators.py        Checkout page selectors
tests/
  test_login.py                Successful and unsuccessful login tests
  test_cart_checkout.py        Cart removal and checkout tests
conftest.py                    Shared browser, page, login, and screenshot fixtures
pytest.ini                     Pytest discovery, options, and markers
requirements.txt               Python package dependencies
.env.example                   Example local configuration
```

## How a test runs

1. Pytest discovers files whose names match the `test_*.py` pattern in
   `tests/`, as configured in `pytest.ini`. This is a filename pattern, not a
   PowerShell command; run tests with `python -m pytest` (see [Run the tests](#run-the-tests)).
2. The shared `browser` fixture selects Chromium, Firefox, or WebKit from
   `PLAYWRIGHT_BROWSER`, then starts that browser using the configured
   headless setting. The browser is shared for the test session and closed at
   the end.
3. The `page` fixture creates a fresh browser context and page for each test,
   sets a 1440 x 900 viewport and the configured action timeout, and closes
   the context after the test.
4. The `login_page` and `logged_in_inventory_page` fixtures open SauceDemo and,
   when requested, log in using the configured credentials.
5. Test code calls page-object methods. Page objects use locator classes so
   selectors are maintained separately from browser actions and assertions.
6. Pytest writes Allure result JSON files into `allure-results`. If a test
   fails, `conftest.py` attaches a full-page screenshot to that test's Allure
   results.

## Requirements and tools

### Required

- Windows 10 or 11 with PowerShell.
- Python 3.9 or newer and the Python launcher (`py`). The framework has also
  been run with Python 3.15.
- Internet access to install the Python packages and Playwright browser, and
  to reach the SauceDemo site.
- Git, if cloning the repository from a Git remote.

The Python packages used by this project are declared in `requirements.txt`:

- `pytest` runs and discovers the tests.
- `playwright` controls the browser.
- `pytest-playwright` provides Playwright pytest integration and the `--headed`
  command-line option.
- `allure-pytest` writes Allure test results.
- `python-dotenv` loads local settings from `.env`.

### Recommended editor setup

Visual Studio Code is optional; the tests also run from PowerShell. If using
VS Code, install Microsoft's **Python** extension (`ms-python.python`) and
select the project's `.venv` interpreter. A separate Playwright VS Code
extension is not required to run this pytest framework.

### Optional: Allure report viewer

The `allure-pytest` Python package creates result files, but it does **not**
install the `allure` command-line application used to view them. Install the
Allure CLI separately if you want to serve or generate an HTML report. The
commands below use Scoop, a Windows package manager. Allure CLI also needs a
Java runtime available on `PATH`.

## Clone and install

Open PowerShell and replace `<repository-url>` and `<repository-folder>` with
the Git remote and folder name for this project:

```powershell
git clone <repository-url>
cd <repository-folder>
```

Create a virtual environment, install dependencies, and install the Chromium
browser used by default:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env
```

If PowerShell reports that `Activate.ps1` cannot run because script execution
is disabled, allow local scripts for the current Windows user, then activate
the environment again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

Activation is optional. You can run commands using the environment's Python
directly, for example:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Configuration

The `.env` file is local and ignored by Git. Start with `.env.example`; edit
`.env` to change the application URL, credentials, or browser settings.

| Variable | Default | Purpose |
| --- | --- | --- |
| `SAUCEDEMO_BASE_URL` | `https://www.saucedemo.com` | Application base URL. |
| `SAUCEDEMO_USERNAME` | `standard_user` | Login username. |
| `SAUCEDEMO_PASSWORD` | `secret_sauce` | Login password. |
| `PLAYWRIGHT_BROWSER` | `chromium` | Browser engine: `chromium`, `firefox`, or `webkit`. |
| `PLAYWRIGHT_HEADLESS` | `true` | Run without a visible browser by default. |
| `PLAYWRIGHT_TIMEOUT_MS` | `10000` | Default timeout, in milliseconds, for Playwright page actions. |

The settings are loaded in `config/settings.py`. Boolean values for
`PLAYWRIGHT_HEADLESS` accept `1`, `true`, `yes`, or `on` (case-insensitive) as
true; other provided values are treated as false.

Chromium is installed by the setup commands above. If changing
`PLAYWRIGHT_BROWSER`, install its browser as well:

```powershell
python -m playwright install firefox
# or
python -m playwright install webkit
```

## Run the tests

Run all tests headlessly:

```powershell
python -m pytest
```

Show the browser for one run, even when `.env` has
`PLAYWRIGHT_HEADLESS=true`:

```powershell
python -m pytest --headed
```

Run a specific test file:

```powershell
python -m pytest tests\test_login.py
python -m pytest tests\test_cart_checkout.py
```

Run just the checkout scenario with a visible browser:

```powershell
python -m pytest --headed tests\test_cart_checkout.py::test_user_can_complete_checkout
```

Run tests marked as smoke tests:

```powershell
python -m pytest -m smoke
```

If the virtual environment is not activated, use
`.\.venv\Scripts\python.exe -m pytest` in place of `python -m pytest`.

## View the Allure report

Every pytest run writes Allure result files to `allure-results`, because the
pytest configuration includes `--alluredir=allure-results`. The directory
contains raw test results; it is not the browsable HTML report.

To install the Allure CLI with Scoop, first install Scoop if it is not already
available. Follow the installation instructions on
[the official Scoop website](https://scoop.sh/), then close and reopen
PowerShell. Install and verify Allure:

```powershell
scoop install allure
allure --version
java -version
```

From the project root, serve the results in a browser (the report is temporary
and generated for this server session):

```powershell
allure serve allure-results
```

To generate a report that remains on disk and then open it:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

The generated HTML report is stored in `allure-report` in the project root.
Generate it again after a new test run to refresh its contents. Both
`allure-results` and `allure-report` are ignored by Git.

## Troubleshooting

### `py` is not recognized

Install Python and its Windows launcher, then reopen PowerShell. Confirm
availability with:

```powershell
py --version
```

### `pytest` is not recognized

Activate `.venv`, or call pytest through the virtual environment's Python:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

If the environment has not been created, run the setup commands above.

### Playwright says a browser executable is missing

Install the browser binary for the configured engine:

```powershell
python -m playwright install chromium
```

### `allure` or `scoop` is not recognized

Allure CLI and Scoop are separate from the Python virtual environment.
Install Scoop using its official setup instructions, install Allure with
`scoop install allure`, and reopen PowerShell so the updated `PATH` is loaded.

### The browser does not appear

Run pytest with `--headed`:

```powershell
python -m pytest --headed
```

### Tests cannot reach SauceDemo

The tests require network access to the configured `SAUCEDEMO_BASE_URL`.
Check that the URL in `.env` is reachable and that the configured demo
credentials are valid.
