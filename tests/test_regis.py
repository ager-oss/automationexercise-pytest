# tests/test_regis.py
from pages.auth_page import AuthPage

def test_successful_registration_and_login(login):
    """
    Menguji keberhasilan proses registrasi dinamis 
    dan memastikan user berhasil masuk ke dasbor utama.
    """
    page = login
    
    # Inisialisasi halaman POM autentikasi
    auth_page = AuthPage(page)
    
    print("\n[VERIFIKASI REGISTRASI] Memeriksa status login akun baru...")
    
    # 1. Assertion: Pastikan menu atas menampilkan status 'Logged in as [Nama User]'
    auth_page.verify_logged_in_status()
    
    print("[SUKSES] Akun dinamis terverifikasi aktif di dalam sistem website!")
