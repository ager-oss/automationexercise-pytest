from pages.auth_page import AuthPage


def test_successful_login(login):
    """Verifikasi bahwa user yang sudah terdaftar terlihat sudah login."""
    page = login
    auth_page = AuthPage(page)

    auth_page.verify_logged_in_status()
    print("[SUKSES] User berhasil login dan status login terverifikasi.")
