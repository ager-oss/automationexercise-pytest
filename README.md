# AutomationExercise Pytest

[![CI](https://github.com/ager-oss/automationexercise-pytest/actions/workflows/pytest.yml/badge.svg)](https://github.com/ager-oss/automationexercise-pytest/actions/workflows/pytest.yml)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green)](https://github.com/ager-oss/automationexercise-pytest/releases/tag/v1.0.0)

Project otomasi UI menggunakan Python, Pytest, dan Playwright untuk menguji alur autentikasi di [Automation Exercise](https://automationexercise.com).

## Fitur

- Signup / register akun baru
- Login user terdaftar
- Logout
- Delete account
- Validasi status login dan account lifecycle

## Struktur Project

- `conftest.py` : fixture untuk membuat sesi login baru per test
- `pages/` : page object model untuk flow auth
- `tests/` : test case pytest

## Persiapan

1. Buat environment virtual dan aktifkan.
2. Install dependency:

```bash
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## Menjalankan Test

```bash
pytest -q
```

Untuk mengecek coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

Untuk mode lokal dengan browser terlihat:

```bash
$env:PLAYWRIGHT_HEADLESS="false"
pytest -q
```

Untuk environment CI/headless:

```bash
$env:CI="true"
pytest -q
```

## Workflow Git

- `main` : branch stabil dan siap untuk release
- `develop` : branch pengembangan dan validasi sebelum merge ke `main`

## Changelog

### v1.0.0

- Setup project automation dengan Python + Playwright
- Implementasi test login, logout, signup, delete account, dan invalid login
- Setup CI dengan GitHub Actions
- Setup coverage report dengan pytest-cov
- Struktur Page Object Model untuk auth flow
- Dokumentasi dan PR template

## Catatan

Project ini sudah menggunakan fixture yang membuat akun baru setiap test agar tidak terjadi stale auth state.
