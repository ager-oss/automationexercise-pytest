from pages.auth_page import AuthPage


def test_successful_logout(login):
    """Verifikasi bahwa user dapat logout dari sesi yang aktif."""
    page = login
    auth_page = AuthPage(page)

    auth_page.logout()
    print("[SUKSES] User berhasil logout dari aplikasi.")
