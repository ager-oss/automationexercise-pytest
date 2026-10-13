# Laporan Hasil Testing

## 1. Tujuan
Melakukan validasi otomatis terhadap fitur website AutomationExercise menggunakan framework Pytest dan Playwright.

## 2. Lingkungan Pengujian
- OS: Windows
- Bahasa: Python
- Framework: Pytest
- Browser Automation: Playwright
- Virtual environment: `.venv`

## 3. Perintah Pengujian
```bash
.\.venv\Scripts\python.exe -m pytest -q
```

## 4. Hasil Pengujian
Hasil eksekusi terbaru yang berhasil diverifikasi adalah:

```text
............                                                             [100%]
12 passed in 133.71s (0:02:13)
```

## 5. Ringkasan Hasil
- Total test: 12
- Status: Passed
- Persentase keberhasilan: 100%
- Durasi total: 133.71 detik

## 6. Daftar Test yang Diuji
- test_add_to_cart.py
- test_auth_flow.py
- test_checkout.py
- test_contact_us.py
- test_delete_account.py
- test_invalid_login.py
- test_login.py
- test_logout.py
- test_payment.py
- test_products.py
- test_regis.py
- test_search_product.py

## 7. Laporan HTML
Untuk kebutuhan visualisasi dan portfolio, hasil test juga dapat dibuat dalam format HTML menggunakan plugin pytest-html.

```bash
pytest --html=report.html --self-contained-html -q
```

Hasilnya akan menghasilkan file `report.html` yang dapat dibuka langsung di browser.

## 8. Kesimpulan
Semua skenario pengujian yang dibuat berhasil dijalankan tanpa gagal. Proyek ini telah lolos validasi otomatis dan siap digunakan sebagai dasar pengembangan lanjutan serta dokumentasi portfolio.