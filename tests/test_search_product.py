import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import expect

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "test_data.json"


def _load_search_terms():
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data["search_terms"]


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


@pytest.mark.parametrize("search_term", _load_search_terms())
def test_search_product_by_name(playwright, search_term):
    """Verifikasi fitur pencarian produk bekerja untuk beberapa keyword yang dibaca dari data JSON."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        _assert_site_available(page)
        page.goto("https://automationexercise.com/products", wait_until="domcontentloaded", timeout=60000)
        expect(page.get_by_role("heading", name="All Products")).to_be_visible()

        page.locator("#search_product").fill(search_term)
        _safe_click(page.locator("#submit_search"))

        expect(page.get_by_text("Searched Products")).to_be_visible()
        visible_result = page.locator("div.productinfo").filter(has_text=search_term).first
        expect(visible_result).to_be_visible()
        print(f"[SUKSES] Produk '{search_term}' berhasil ditemukan melalui fitur search.")
    finally:
        context.close()
        browser.close()
