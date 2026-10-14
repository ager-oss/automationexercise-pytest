# pages/base_page.py
import pytest
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def _safe_click(self, locator, timeout=20000, **kwargs):
        """Klik yang aman untuk target yang kadang tertutup overlay atau animasi."""
        for force in (False, True):
            try:
                locator.scroll_into_view_if_needed()
                locator.click(timeout=timeout, force=force, **kwargs)
                return
            except Exception:
                pass

        locator.evaluate("element => element.click()")

    def _assert_site_available(self):
        """Abaikan bila situs sedang down karena error eksternal."""
        try:
            self.page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=30000)
        except Exception as exc:  # pragma: no cover - dependensi eksternal
            pytest.skip(f"AutomationExercise tidak dapat dijangkau: {exc}")

        body_text = self.page.locator("body").inner_text()
        lowered = body_text.lower()
        if "cloudflare" in lowered or "error code 520" in lowered or "unknown error" in lowered:
            pytest.skip("AutomationExercise sedang tidak tersedia karena Cloudflare 520.")

    def open_home(self):
        """Buka halaman utama website."""
        self.page.goto("https://automationexercise.com", wait_until="domcontentloaded", timeout=30000)
