import json
import os
from pathlib import Path

import pytest

from pages.auth_page import AuthPage

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "test_data.json"


def _load_invalid_login_cases():
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return [(item["email"], item["password"]) for item in data["invalid_login"]]


@pytest.mark.parametrize(("email", "password"), _load_invalid_login_cases())
def test_invalid_login_shows_error(playwright, email, password):
    """Verifikasi kombinasi invalid login yang dibaca dari file data JSON pusat."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    try:
        auth_page = AuthPage(page)
        auth_page.login_with_invalid_credentials(email, password)
        print(f"[SUKSES] Invalid login case: email={email!r}, password={password!r}")
    finally:
        context.close()
        browser.close()
