import pytest
from playwright.sync_api import Page
from pages.auth_exercise_page import AuthExercisePage  # Mengimpor dari folder pages
import time

def test_user_registration_and_deletion(page: Page):
    auth_page = AuthExercisePage(page)
    
    # Membuat email acak berbasis timestamp agar tidak duplikat saat tes diulang
    email_unik = f"akuntest_{int(time.time())}@gmail.com"
    
    # 1. Jalankan Alur Navigasi
    auth_page.navigate()
    auth_page.go_to_signup()
    
    # 2. Registrasi Tahap Awal
    auth_page.submit_initial_signup("akuntest", email_unik)
    
    # 3. Isi Detail Informasi Akun
    auth_page.fill_account_details("12345", "17", "9", "2007")
    
    # 4. Isi Data Alamat Lengkap
    auth_page.fill_address_details(
        first="akun", 
        last="test", 
        company="test123", 
        addr1="test123", 
        addr2="test1234", 
        country="New Zealand", 
        state="swiss", 
        city="kanada", 
        zip_code="213", 
        mobile="214124124"
    )
    
    # 5. Verifikasi Pendaftaran & Status Login
    auth_page.verify_and_continue_registration("akuntest")
    
    # 6. Hapus Akun (Pembersihan Data)
    auth_page.clean_up_account()
