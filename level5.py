import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://datatables.net/examples/basic_init/alt_pagination.html")
    page.get_by_label("entries per page").select_option("100")

     # Chờ bảng xuất hiện
    # Chờ bảng xuất hiện
    page.wait_for_selector("#example")

    # Lấy header
    headers = page.locator("#example thead th").all_text_contents()
    print("Headers:", headers)
    pos = headers.index("Name")

    # Lấy dữ liệu từng hàng
    rows = page.locator("#example tbody tr")
    for i in range(rows.count()):
        cells = rows.nth(i).locator("td").all_text_contents()
        print(cells[pos])

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
