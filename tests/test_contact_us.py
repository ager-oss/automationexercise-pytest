import os
import time
from pathlib import Path

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


def test_contact_us_form_submit(playwright):
    """Verifikasi form Contact Us dapat dikirim dengan sukses."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()
    temp_file = Path("contact_upload.txt")

    try:
        _assert_site_available(page)
        expect(page.get_by_role("link", name="Contact us")).to_be_visible()
        page.get_by_role("link", name="Contact us").click()

        expect(page.get_by_role("heading", name="Get In Touch")).to_be_visible()

        page.locator('[data-qa="name"]').fill("Tester Automation")
        page.locator('[data-qa="email"]').fill(f"tester{int(time.time())}@example.com")
        page.locator('[data-qa="subject"]').fill("Testing contact form")
        page.locator('[data-qa="message"]').fill("Halo, ini adalah test otomatis dari Playwright.")

        temp_file.write_text("Automation Exercise contact test", encoding="utf-8")
        page.locator('input[name="upload_file"]').set_input_files(str(temp_file))

        page.on("dialog", lambda dialog: dialog.accept())
        page.locator('[data-qa="submit-button"]').click()
        expect(page.locator(".status.alert-success")).to_contain_text("Success! Your details have been submitted successfully.")
        expect(page.locator("#form-section a.btn-success")).to_be_visible()
        print("[SUKSES] Form Contact Us memunculkan konfirmasi dan berhasil menampilkan status sukses.")
    finally:
        if temp_file.exists():
            temp_file.unlink()
        context.close()
        browser.close()
