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


def test_add_first_product_to_cart(playwright):
    """Verifikasi user dapat menambahkan produk pertama ke cart dari halaman produk."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        _assert_site_available(page)
        page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
        expect(page.get_by_role("heading", name="All Products")).to_be_visible()

        page.locator("a[data-product-id='1']").first.click()
        expect(page.locator("div.modal")).to_be_visible()
        expect(page.locator("div.modal")).to_contain_text("Your product has been added to cart.")
        print("[SUKSES] Produk berhasil ditambahkan ke cart.")
    finally:
        context.close()
        browser.close()
