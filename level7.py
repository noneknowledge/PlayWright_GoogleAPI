# requirements:
#   pip install playwright
#   playwright install

import os
from pathlib import Path
from playwright.sync_api import sync_playwright

DATASET_NAME = "DataTables_Buttons_HTML5"
BASE_URL = "https://datatables.net/extensions/buttons/examples/html5/simple.html"

def main():
    # Tạo thư mục lưu tải xuống: downloads/<Dataset>/
    download_dir = Path("downloads") / DATASET_NAME
    download_dir.mkdir(parents=True, exist_ok=True)

    downloaded_files = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Bật accept_downloads để Playwright xử lý download
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Truy cập trang demo
        page.goto(BASE_URL, wait_until="domcontentloaded")

        # Đảm bảo các nút export đã hiển thị
        page.wait_for_selector("div.dt-buttons button", state="visible")

        # Danh sách các nút cần click: CSV và Excel (HTML5)
        # Selector phổ biến của Buttons: .buttons-csv và .buttons-excel
        export_targets = [
            {"label": "CSV", "selector": "button.buttons-csv"},
            {"label": "Excel", "selector": "button.buttons-excel"},
        ]

        for target in export_targets:
            # Một số trang có nhiều bảng/nút; chọn nút đầu tiên phù hợp
            locator = page.locator(target["selector"]).first

            # Bắt sự kiện download khi click
            with page.expect_download() as download_info:
                locator.click()
            download = download_info.value

            # Xác định tên file mặc định và lưu dưới downloads/<Dataset>/
            suggested_name = download.suggested_filename
            save_path = download_dir / suggested_name

            # Lưu file
            download.save_as(str(save_path))
            downloaded_files.append(save_path)

        # Đóng trình duyệt
        context.close()
        browser.close()

    # Acceptance: Files exist; script prints "Downloaded n file(s)."
    existing = [p for p in downloaded_files if p.exists()]
    print(f"Downloaded {len(existing)} file(s).")
    for p in existing:
        print(f"- {p}")

if __name__ == "__main__":
    main()
