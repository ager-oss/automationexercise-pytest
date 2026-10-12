import os
import random
import time

import pytest
from playwright.sync_api import expect


def _create_new_account(page, name: str, email: str):
    """Membuat akun baru dan menunggu sampai status login valid muncul."""
    page.goto("https://automationexercise.com")
    expect(page.get_by_role("link", name="Signup / Login")).to_be_visible()
    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form[action='/signup'] input[name='email']").fill(email)
    page.locator("form[action='/signup'] button[type='submit']").click()

    expect(page.get_by_text("Enter Account Information")).to_be_visible()
    page.locator("#password").fill("Rahasia123!")
    page.locator("#first_name").fill("Joko")
    page.locator("#last_name").fill("Tester")
    page.locator("#address1").fill("Gedung Cyber Cyber, Lantai 5")
    page.locator("#country").select_option("United States")
    page.locator("#state").fill("DKI Jakarta")
    page.locator("#city").fill("Jakarta Barat")
    page.locator("#zipcode").fill("11730")
    page.locator("#mobile_number").fill("081234567890")

    page.locator("button[data-qa='create-account']").click()
    expect(page.get_by_text("Account Created!")).to_be_visible()
    page.locator("[data-qa='continue-button']").click()
    expect(page.get_by_text(f"Logged in as {name}")).to_be_visible()


@pytest.fixture(scope="function")
def login(playwright):
    """Fixture login yang selalu membuat sesi valid baru per test."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    unique_id = int(time.time())
    dynamic_name = f"Tester Automation {random.randint(1, 100)}"
    dynamic_email = f"user.tester{unique_id}@example.com"

    _create_new_account(page, dynamic_name, dynamic_email)

    yield page

    context.close()
    browser.close()
