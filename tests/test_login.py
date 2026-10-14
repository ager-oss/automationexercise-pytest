import json
import os
import uuid
from pathlib import Path

import pytest

from conftest import _create_new_account
from pages.auth_page import AuthPage

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "test_data.json"


def _load_valid_login_cases():
    with DATA_FILE.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    return [
        (item["name"], item["base_email"], item["password"]) for item in data["valid_users"]
    ]


@pytest.mark.parametrize(("name", "base_email", "password"), _load_valid_login_cases())
def test_successful_login(playwright, name, base_email, password):
    """Verifikasi login berhasil berdasarkan data valid dari file JSON pusat dengan email unik per eksekusi."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()
    unique_email = f"{base_email}.{uuid.uuid4().hex[:8]}@example.com"

    try:
        _create_new_account(page, name, unique_email)
        auth_page = AuthPage(page)
        auth_page.verify_logged_in_status()
        print(f"[SUKSES] Valid login case: email={unique_email!r}, password={password!r}")
    finally:
        context.close()
        browser.close()
