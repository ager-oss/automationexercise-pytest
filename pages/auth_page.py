# pages/auth_page.py
import pytest
from playwright.sync_api import Page, expect

class AuthPage:
    def __init__(self, page: Page):
        self.page = page
        # Selector yang sesuai dengan struktur real halaman: teks 'Logged in as ...'
        # muncul di banner/header navigasi utama, bukan di elemen dengan id #header.
        self.logged_in_user_text = page.get_by_text("Logged in as", exact=False)
        self.delete_account_link = page.get_by_role("link", name="Delete Account")

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

    def go_to_login(self):
        """Masuk ke halaman login/signup"""
        self._assert_site_available()
        expect(self.page.get_by_role("link", name="Signup / Login")).to_be_visible()
        self.page.get_by_role("link", name="Signup / Login").click()
        expect(self.page.get_by_role("heading", name="Login to your account")).to_be_visible()

    def login(self, email: str, password: str):
        """Melakukan login dengan email dan password"""
        self.go_to_login()
        self.page.locator("form[action='/login'] input[name='email']").fill(email)
        self.page.locator("form[action='/login'] input[name='password']").fill(password)
        self.page.locator("form[action='/login'] button[type='submit']").click()
        self.verify_logged_in_status()

    def login_with_invalid_credentials(self, email: str, password: str):
        """Mencoba login dengan kredensial yang salah dan memvalidasi pesan error."""
        self.go_to_login()
        self.page.locator("form[action='/login'] input[name='email']").fill(email)
        self.page.locator("form[action='/login'] input[name='password']").fill(password)
        self.page.locator("form[action='/login'] button[type='submit']").click()
        expect(self.page.get_by_text("Your email or password is incorrect!")).to_be_visible()

    def logout(self):
        """Keluar dari sesi login yang sedang aktif."""
        self.page.get_by_role("link", name="Logout").click()
        expect(self.page.get_by_role("heading", name="Login to your account")).to_be_visible()

    def delete_account(self):
        """Menghapus akun yang sedang aktif."""
        self.page.get_by_role("link", name="Delete Account").click()
        expect(self.page.get_by_text("Account Deleted!")).to_be_visible()
        self.page.get_by_role("link", name="Continue").click()

    def verify_logged_in_status(self):
        """Memastikan teks 'Logged in as' muncul di menu navigasi atas"""
        expect(self.logged_in_user_text).to_be_visible()

        raw_text = self.logged_in_user_text.text_content() or ""
        print(f"  > Konfirmasi Visual: {raw_text.strip()}")
