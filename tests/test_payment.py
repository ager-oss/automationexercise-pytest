import os

import pytest
from playwright.sync_api import expect

from conftest import capture_screenshot


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


def test_place_order_and_payment(playwright):
    """Verifikasi user login dapat melakukan place order dengan input payment valid."""
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
        capture_screenshot(page, "payment_01_signup_page")

        unique_name = "Tester Payment"
        unique_email = f"payment.{os.urandom(4).hex()}@example.com"
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
        capture_screenshot(page, "payment_02_after_account_created")

        page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
        page.locator("a[data-product-id='1']").first.click()
        expect(page.locator("div.modal")).to_be_visible()
        expect(page.locator("div.modal")).to_contain_text("Your product has been added to cart.")

        page.goto("https://automationexercise.com/view_cart", wait_until="domcontentloaded", timeout=60000)
        expect(page.get_by_text("Blue Top")).to_be_visible()
        page.locator("a.check_out").click()
        expect(page.get_by_role("link", name="Place Order")).to_be_visible()
        page.get_by_role("link", name="Place Order").click()

        expect(page.get_by_role("heading", name="Payment")).to_be_visible()
        page.locator("input[name='name_on_card']").fill("Joko Tester")
        page.locator("input[name='card_number']").fill("4111111111111111")
        page.locator("input[name='cvc']").fill("123")
        page.locator("input[name='expiry_month']").fill("12")
        page.locator("input[name='expiry_year']").fill("2035")
        page.locator("button[data-qa='pay-button']").click()

        expect(page.get_by_role("heading", name="Order Placed!")).to_be_visible()
        expect(page.get_by_text("Congratulations! Your order has been confirmed!")).to_be_visible()
        expect(page.get_by_role("link", name="Continue")).to_be_visible()
        capture_screenshot(page, "payment_03_order_success")
        print("[SUKSES] Place order selesai dan pembayaran berhasil diproses.")
    finally:
        context.close()
        browser.close()
