import os
import time
from pathlib import Path

from playwright.sync_api import expect


def test_contact_us_form_submit(playwright):
    """Verifikasi form Contact Us dapat dikirim dengan sukses."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()
    temp_file = Path("contact_upload.txt")
    dialog_message = {"value": ""}

    try:
        page.goto("https://automationexercise.com")
        expect(page.get_by_role("link", name="Contact us")).to_be_visible()
        page.get_by_role("link", name="Contact us").click()

        expect(page.get_by_role("heading", name="Get In Touch")).to_be_visible()

        page.locator('[data-qa="name"]').fill("Tester Automation")
        page.locator('[data-qa="email"]').fill(f"tester{int(time.time())}@example.com")
        page.locator('[data-qa="subject"]').fill("Testing contact form")
        page.locator('[data-qa="message"]').fill("Halo, ini adalah test otomatis dari Playwright.")

        temp_file.write_text("Automation Exercise contact test", encoding="utf-8")
        page.locator('input[name="upload_file"]').set_input_files(str(temp_file))

        page.once(
            "dialog",
            lambda dialog: (dialog_message.update({"value": dialog.message}), dialog.accept()),
        )
        page.locator('[data-qa="submit-button"]').click()

        assert dialog_message["value"] == "Press OK to proceed!"
        print("[SUKSES] Form Contact Us memunculkan alert konfirmasi dan berhasil diterima.")
    finally:
        if temp_file.exists():
            temp_file.unlink()
        context.close()
        browser.close()
