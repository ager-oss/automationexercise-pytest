import os

import pytest
from playwright.sync_api import expect


def _assert_site_available(page):
    """Skip bila situs sedang mengalami error eksternal seperti Cloudflare 520."""
    try:
        page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=30000)
    except Exception as exc:  # pragma: no cover - dependensi eksternal
        pytest.skip(f"AutomationExercise tidak dapat dijangkau: {exc}")

    body_text = page.locator("body").inner_text()
    lowered = body_text.lower()
    if "cloudflare" in lowered or "error code 520" in lowered or "unknown error" in lowered:
        pytest.skip("AutomationExercise sedang tidak tersedia karena Cloudflare 520.")


def test_checkout_from_cart(playwright):
    """Verifikasi user logged in dapat melakukan checkout dari cart."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        _assert_site_available(page)
        page.goto("https://automationexercise.com")
        expect(page.get_by_role("link", name="Signup / Login")).to_be_visible()
        page.get_by_role("link", name="Signup / Login").click()

        unique_name = "Tester Checkout" 
        unique_email = f"checkout.{os.urandom(4).hex()}@example.com"
        page.get_by_role("textbox", name="Name").fill(unique_name)
        page.locator("form[action='/signup'] input[name='email']").fill(unique_email)
        page.locator("form[action='/signup'] button[type='submit']").click()

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
        page.locator("[data-qa='continue-button']").click()

        page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
        page.locator("a[data-product-id='1']").first.click()
        page.wait_for_timeout(1500)

        page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded", timeout=60000)
        expect(page.get_by_text("Blue Top")).to_be_visible()
        page.locator("a.check_out").click()
        expect(page.get_by_role("heading", name="Address Details")).to_be_visible()
        expect(page.get_by_role("heading", name="Review Your Order")).to_be_visible()
        print("[SUKSES] Checkout dari cart berhasil diakses.")
    finally:
        context.close()
        browser.close()
