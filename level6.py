import asyncio
import random
import time
from playwright.async_api import async_playwright

def record_event(event_name, level=10):
    print(f"[Telemetry] Level {level}: {event_name}")

async def main():
    async with async_playwright() as p:
        # Kết nối tới Chrome qua CDP
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        # Lấy context mặc định
        context = browser.contexts[0]
        page = await context.new_page()

        # Truy cập trang demo
        await page.goto("https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php")

        # 1. Phát hiện widget trong ≤3s
        try:
            await page.wait_for_selector('iframe[src*="recaptcha"]', timeout=3000)
            print("✅ reCAPTCHA widget được phát hiện")
        except:
            print("❌ Không tìm thấy reCAPTCHA trong 3s")
            await browser.close()
            return

        # 2. Tạm dừng và nhắc người dùng/extension giải captcha
        print("⏸️ Vui lòng giải captcha trên trình duyệt...")

        # 3. Chờ đến khi captcha được giải (timeout cấu hình)
        timeout = 60  # có thể chỉnh
        start = time.time()
        solved = False
        while time.time() - start < timeout:
            value = await page.evaluate("document.getElementById('g-recaptcha-response').value")
            if value and value.strip() != "":
                solved = True
                break
            await asyncio.sleep(1)

        if not solved:
            print("❌ Hết thời gian chờ captcha")
            await browser.close()
            return

        # 4. Backoff ngẫu nhiên 5–30s
        backoff = random.randint(5, 30)
        print(f"⌛ Backoff {backoff}s trước khi tiếp tục...")
        await asyncio.sleep(backoff)

        # 5. Ghi telemetry
        record_event("Captcha solved", level=10)

        await browser.close()

asyncio.run(main())
