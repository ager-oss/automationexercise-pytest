import os

import pytest
from playwright.sync_api import expect


def _assert_site_available(page):
    """Skip test bila situs sedang mengalami error eksternal seperti Cloudflare 520."""
    try:
        page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=30000)
    except Exception as exc:  # pragma: no cover - dependensi eksternal
        pytest.skip(f"AutomationExercise tidak dapat dijangkau: {exc}")

    body_text = page.locator("body").inner_text()
    lowered = body_text.lower()
    if "cloudflare" in lowered or "error code 520" in lowered or "unknown error" in lowered:
        pytest.skip("AutomationExercise sedang tidak tersedia karena Cloudflare 520.")


def test_view_first_product_details(playwright):
    """Verifikasi user dapat membuka halaman detail produk dari daftar produk."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        _assert_site_available(page)
        page.goto("https://automationexercise.com/product_details/1", wait_until="domcontentloaded", timeout=60000)
        assert "/product_details/1" in page.url
        expect(page.get_by_text("Blue Top")).to_be_visible()
        expect(page.get_by_text("Category: Women > Tops")).to_be_visible()

        print("[SUKSES] Halaman detail produk berhasil dibuka.")
    finally:
        context.close()
        browser.close()
