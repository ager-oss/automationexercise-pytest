from pages.auth_page import AuthPage


def test_successful_delete_account(login):
    """Verifikasi bahwa user dapat menghapus akun yang sedang aktif."""
    page = login
    auth_page = AuthPage(page)

    auth_page.delete_account()
    print("[SUKSES] Akun berhasil dihapus dari aplikasi.")
