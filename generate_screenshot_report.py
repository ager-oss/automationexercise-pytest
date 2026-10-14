from __future__ import annotations

import html
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
REPORTS_DIR = ROOT / "reports"
JUNIT_XML = REPORTS_DIR / "junit.xml"
OUTPUT_FILE = ROOT / "screenshots_report.html"


def _read_junit_summary():
    summary = {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "error": 0}
    testcases = []

    if not JUNIT_XML.exists():
        return summary, testcases

    try:
        tree = ET.parse(JUNIT_XML)
        root = tree.getroot()
    except ET.ParseError:
        return summary, testcases

    for testcase in root.iter("testcase"):
        name = testcase.attrib.get("name", "unknown")
        classname = testcase.attrib.get("classname", "")
        status = "passed"
        if testcase.find("failure") is not None:
            status = "failed"
        elif testcase.find("error") is not None:
            status = "error"
        elif testcase.find("skipped") is not None:
            status = "skipped"

        summary["total"] += 1
        summary[status] += 1
        testcases.append({
            "name": name,
            "classname": classname,
            "status": status,
        })

    return summary, testcases


def _status_color(status: str) -> str:
    colors = {
        "passed": "#16a34a",
        "failed": "#dc2626",
        "skipped": "#f59e0b",
        "error": "#7c2d12",
    }
    return colors.get(status, "#374151")


def build_report():
    summary, testcases = _read_junit_summary()
    screenshots = sorted(SCREENSHOT_DIR.glob("*.png"))

    if not screenshots:
        screenshot_html = """
        <div style='padding: 18px; background: #fef3c7; border: 1px solid #fbbf24; border-radius: 8px; color: #78350f;'>
            Tidak ada screenshot yang ditemukan. Jalankan test terlebih dahulu agar file PNG dibuat.
        </div>
        """
    else:
        screenshot_cards = []
        for file in screenshots:
            rel_path = file.relative_to(ROOT).as_posix()
            screenshot_cards.append(
                f"""
                <div style='margin-bottom: 22px; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; background: #fff;'>
                    <h3 style='margin: 0 0 10px; font-size: 18px;'>{html.escape(file.stem)}</h3>
                    <img src='{rel_path}' style='max-width: 100%; border-radius: 8px; border: 1px solid #d1d5db;' />
                </div>
                """
            )
        screenshot_html = "\n".join(screenshot_cards)

    summary_cards = "\n".join(
        f"""
        <div style='flex: 1; min-width: 160px; background: #fff; border-radius: 10px; border: 1px solid #e5e7eb; padding: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);'>
            <div style='font-size: 13px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;'>{label}</div>
            <div style='font-size: 32px; font-weight: 700; margin-top: 8px;'>{value}</div>
        </div>
        """
        for label, value in [
            ("Total", summary["total"]),
            ("Passed", summary["passed"]),
            ("Failed", summary["failed"]),
            ("Skipped", summary["skipped"]),
            ("Error", summary["error"]),
        ]
    )

    table_rows = []
    if not testcases:
        table_rows.append(
            """
            <tr>
                <td colspan='3' style='padding: 14px; color: #6b7280;'>Belum ada data test hasil dari JUnit XML.</td>
            </tr>
            """
        )
    else:
        for item in testcases:
            status = item["status"]
            badge_color = _status_color(status)
            table_rows.append(
                f"""
                <tr>
                    <td style='padding: 12px 14px; border-bottom: 1px solid #e5e7eb;'>{html.escape(item['classname']) or '-'}</td>
                    <td style='padding: 12px 14px; border-bottom: 1px solid #e5e7eb;'>{html.escape(item['name'])}</td>
                    <td style='padding: 12px 14px; border-bottom: 1px solid #e5e7eb;'><span style='display:inline-block; padding: 4px 10px; border-radius: 999px; color: #fff; background: {badge_color}; font-weight: 600; text-transform: uppercase;'>{status}</span></td>
                </tr>
                """
            )

    html_content = f"""
    <!DOCTYPE html>
    <html lang='id'>
    <head>
        <meta charset='UTF-8' />
        <meta name='viewport' content='width=device-width, initial-scale=1.0' />
        <title>Laporan Test AutomationExercise</title>
        <style>
            body {{
                margin: 0;
                background: #f5f7fb;
                color: #111827;
                font-family: Arial, sans-serif;
            }}
            .container {{
                max-width: 1200px;
                margin: 30px auto;
                padding: 0 20px 40px;
            }}
            h1 {{
                margin: 0 0 20px;
                font-size: 30px;
            }}
            .summary {{
                display: flex;
                gap: 16px;
                flex-wrap: wrap;
                margin-bottom: 28px;
            }}
            .section {{
                background: #fff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }}
            th {{
                text-align: left;
                padding: 12px 14px;
                border-bottom: 2px solid #d1d5db;
                background: #f3f4f6;
            }}
            td {{
                vertical-align: top;
            }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>Laporan Test AutomationExercise</h1>

            <div class='summary'>
                {summary_cards}
            </div>

            <div class='section'>
                <h2 style='margin-top: 0;'>Status per test case</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Class</th>
                            <th>Test</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>

            <div class='section'>
                <h2 style='margin-top: 0;'>Screenshot</h2>
                {screenshot_html}
            </div>
        </div>
    </body>
    </html>
    """

    OUTPUT_FILE.write_text(html_content, encoding='utf-8')
    print(f"Laporan detail dibuat: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
