import os

from pages.auth_page import AuthPage


def test_invalid_login_shows_error(playwright):
    """Verifikasi bahwa login dengan kredensial salah menampilkan pesan error."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        auth_page = AuthPage(page)
        auth_page.login_with_invalid_credentials("wrong@example.com", "wrongpassword")
        print("[SUKSES] Login dengan kredensial salah menampilkan pesan error yang benar.")
    finally:
        context.close()
        browser.close()
