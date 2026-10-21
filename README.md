# AutomationExercise Web Testing

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7.x-orange)](https://pytest.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2ea44f)](https://playwright.dev/)

A practical web automation project built with Python, Pytest, and Playwright to test the AutomationExercise website end-to-end.

## Overview

This project automates key user flows on the demo e-commerce site, including:

- user registration
- login and invalid login
- logout
- delete account
- products search
- cart and checkout flow
- contact us form
- payment process

The suite uses a Page Object Model (POM) approach to keep the tests readable, reusable, and maintainable.

## Why this project

This repository demonstrates real browser automation for a public web application, including session handling, UI validation, and regression coverage for common user journeys. It is suitable as a portfolio project for QA automation and test engineering roles.

## Tech Stack

- Python 3.11
- Pytest
- Playwright
- GitHub Actions
- pytest-cov

## Project Structure

```text
automationexercise-pytest/
├── conftest.py
├── pages/
│   ├── auth_page.py
│   └── auth_exercise_page.py
├── tests/
│   ├── test_login.py
│   ├── test_logout.py
│   ├── test_regis.py
│   ├── test_invalid_login.py
│   ├── test_delete_account.py
│   ├── test_search_product.py
│   ├── test_add_to_cart.py
│   ├── test_checkout.py
│   ├── test_payment.py
│   ├── test_contact_us.py
│   ├── test_products.py
│   └── test_auth_flow.py
├── requirements.txt
├── REPORT_TESTING.md
├── README.md
├── htmlcov/
└── .github/
```

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

## Run Tests

```bash
pytest -q
```

After a local test run, Pytest automatically opens both `report.html` (the standard pytest-html report) and `screenshots_report.html` (test status and screenshots) in the default browser. In CI, reports are generated without opening a browser.

With coverage:

```bash
pytest --cov=. --cov-report=term-missing -q
```

## Verified Result

The latest validated run is:

```text
............                                                             [100%]
12 passed in 133.71s (0:02:13)
```

## CI / Workflow

This project is structured to support continuous validation using GitHub Actions and can be extended with additional scenarios and reporting.

## Notes

The test suite is intentionally designed to validate real user behavior in a live production-like website and to highlight stable automation practices for browser-based testing.

## Contact

For collaboration, project discussion, or QA automation opportunities, feel free to connect.
