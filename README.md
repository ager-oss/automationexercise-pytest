# AutomationExercise Pytest

[![CI](https://github.com/ager-oss/automationexercise-pytest/actions/workflows/pytest.yml/badge.svg)](https://github.com/ager-oss/automationexercise-pytest/actions/workflows/pytest.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green)](https://github.com/ager-oss/automationexercise-pytest/releases/tag/v1.0.0)

Automation UI testing project built with Python, Pytest, and Playwright for the Automation Exercise website.

## Overview

This project validates the main authentication journey of the application, including:

- user registration
- successful login
- invalid login
- logout
- delete account

The implementation follows a Page Object Model (POM) structure and creates a fresh valid session for each test to avoid stale authentication state.

## How It Works

Each test opens a real browser session with Playwright, navigates to the target website, interacts with the UI elements, and verifies the expected result through assertions. The project uses dedicated page objects to keep the test flow readable and reusable, while fixture-based setup ensures each scenario starts from a clean authenticated or unauthenticated state.

This approach makes the suite suitable for UI regression testing, authentication validation, and behavior verification in a real web application.

## Tech Stack

- Python 3.11
- Pytest
- Playwright
- GitHub Actions
- pytest-cov

## Project Structure

- `conftest.py` — session setup and account creation fixture
- `pages/` — POM classes for auth actions
- `tests/` — automated test cases
- `.github/workflows/pytest.yml` — CI pipeline
- `htmlcov/` — generated test coverage report

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Run Tests

```bash
pytest -q
```

Run with coverage:

```bash
pytest --cov=. --cov-report=term-missing -q
```

Generate HTML coverage report:

```bash
pytest --cov=. --cov-report=html -q
```

## CI and Git Workflow

- `main` — stable release branch
- `develop` — working branch for updates and validation

## Verified Result

Current test suite status:

```bash
6 passed in 66.81s
```

## Project Status

This project is currently in a stable state and is ready for use as a reference automation suite for UI testing and authentication flows. The implementation includes a robust session setup, reliable selectors, error validation, and a CI-ready configuration.

## Changelog

### v1.0.0

- Initial project setup
- Authentication automation for registration and login flows
- Logout and delete account scenarios
- Invalid login validation
- CI workflow and coverage integration
- Documentation and PR template

## Notes

This project is intended to demonstrate reliable browser automation and test structure for UI validation in a real public web app.
