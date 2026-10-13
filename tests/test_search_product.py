import os

import pytest
from playwright.sync_api import expect


def _safe_click(locator, timeout=20000, **kwargs):
    """Klik yang aman saat halaman menampilkan overlay atau animasi yang mengganggu klik normal."""
    for force in (False, True):
        try:
            locator.scroll_into_view_if_needed()
            locator.click(timeout=timeout, force=force, **kwargs)
            return
        except Exception:
            pass

    locator.evaluate("element => element.click()")


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


def test_search_product_by_name(playwright):
    """Verifikasi fitur pencarian produk bekerja dan menampilkan produk yang dicari."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        _assert_site_available(page)
        page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
        expect(page.get_by_role("heading", name="All Products")).to_be_visible()

        page.locator("#search_product").fill("Blue Top")
        _safe_click(page.locator("#submit_search"))

        expect(page.get_by_text("Searched Products")).to_be_visible()
        expect(page.get_by_text("Blue Top").first).to_be_visible()
        print("[SUKSES] Produk 'Blue Top' berhasil ditemukan melalui fitur search.")
    finally:
        context.close()
        browser.close()
