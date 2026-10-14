from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
OUTPUT_FILE = ROOT / "screenshots_report.html"


def build_report():
    files = sorted(SCREENSHOT_DIR.glob("*.png"))

    if not files:
        body = """
        <div style='padding: 24px; font-family: Arial, sans-serif;'>
            <h2>Tidak ada screenshot</h2>
            <p>Folder screenshots masih kosong. Jalankan test terlebih dahulu agar file PNG terbentuk.</p>
        </div>
        """
    else:
        cards = []
        for file in files:
            rel_path = file.relative_to(ROOT).as_posix()
            cards.append(
                f"""
                <div style='margin-bottom: 24px; border: 1px solid #ddd; border-radius: 10px; padding: 16px; background: #fff;'>
                    <h3 style='margin: 0 0 12px; font-size: 18px;'>{html.escape(file.stem)}</h3>
                    <img src='{rel_path}' style='max-width: 100%; border: 1px solid #ccc; border-radius: 8px;' />
                </div>
                """
            )
        body = "\n".join(cards)

    html_content = f"""
    <!DOCTYPE html>
    <html lang='id'>
    <head>
        <meta charset='UTF-8' />
        <meta name='viewport' content='width=device-width, initial-scale=1.0' />
        <title>Laporan Screenshot AutomationExercise</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f5f7fb;
                color: #1f2937;
            }}
            .container {{
                max-width: 1100px;
                margin: 40px auto;
                padding: 0 20px;
            }}
            h1 {{
                margin-bottom: 24px;
                font-size: 30px;
            }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>Laporan Screenshot AutomationExercise</h1>
            {body}
        </div>
    </body>
    </html>
    """

    OUTPUT_FILE.write_text(html_content, encoding='utf-8')
    print(f"Laporan screenshot dibuat: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
