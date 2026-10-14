import os
import random
import re
import time

import pytest
from playwright.sync_api import expect

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")


def capture_screenshot(page, name: str, *, full_page: bool = True):
    """Simpan screenshot halaman ke folder screenshots/ agar mudah debugging visual."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_") or "screenshot"
    file_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")
    page.screenshot(path=file_path, full_page=full_page)
    return file_path


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Ambil screenshot otomatis saat test gagal dan halaman masih tersedia."""
    if call.when != "call" or call.excinfo is None:
        return

    funcargs = getattr(item, "funcargs", {}) or {}
    page = None
    for fixture_name in ("page", "login"):
        page = funcargs.get(fixture_name)
        if page is not None:
            break

    if page is None or not hasattr(page, "screenshot"):
        return

    try:
        file_path = capture_screenshot(page, f"failed_{item.name}")
        print(f"SCREENSHOT_TAKEN={file_path}")
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report screenshot otomatis setelah keseluruhan sesi test selesai."""
    try:
        from generate_screenshot_report import build_report

        build_report()
    except Exception as exc:  # pragma: no cover - pelaporan non-fatal
        print(f"REPORT_WARNING={exc}")


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


def _create_new_account(page, name: str, email: str):
    """Membuat akun baru dan menunggu sampai status login valid muncul."""
    _assert_site_available(page)
    expect(page.get_by_role("link", name="Signup / Login")).to_be_visible()
    page.get_by_role("link", name="Signup / Login").click()
    expect(page.get_by_role("heading", name="New User Signup!")).to_be_visible()

    page.get_by_role("textbox", name="Name").fill(name)
    page.locator("form[action='/signup'] input[name='email']").fill(email)
    page.locator("form[action='/signup'] button[type='submit']").click()

    expect(page.get_by_text("Enter Account Information")).to_be_visible()
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
    expect(page.get_by_text("Account Created!")).to_be_visible()
    page.locator("[data-qa='continue-button']").click()
    expect(page.get_by_text(f"Logged in as {name}")).to_be_visible()


@pytest.fixture(scope="function")
def login(playwright):
    """Fixture login yang selalu membuat sesi valid baru per test."""
    headless_flag = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes"}
    ci_flag = os.getenv("CI", "").lower() == "true"
    browser = playwright.chromium.launch(headless=headless_flag or ci_flag)
    context = browser.new_context()
    page = context.new_page()

    unique_id = int(time.time())
    dynamic_name = f"Tester Automation {random.randint(1, 100)}"
    dynamic_email = f"user.tester{unique_id}@example.com"

    _create_new_account(page, dynamic_name, dynamic_email)

    yield page

    context.close()
    browser.close()
