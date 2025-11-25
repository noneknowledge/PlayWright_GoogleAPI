import json
from playwright.async_api import Playwright, async_playwright, expect, Page
import asyncio
from dotenv import dotenv_values

config = dotenv_values(".env")


async def getPreviusContent(page:Page):
    await page.get_by_role("menuitem", name="Hiển thị lịch sử chỉnh sửa").click()

    await page.wait_for_timeout(1000)
    
    popUp = await page.locator(".docs-blameview-valuecontainer").nth(0).text_content()
    while not popUp:  
        print("Loading...")
        popUp = await page.locator(".docs-blameview-valuecontainer").nth(0).text_content()
        await page.wait_for_timeout(500)
    timeStamp = await page.locator(".docs-blameview-timestamp").nth(0).text_content()
    content =  popUp.split('"')
    print("Done")

    keyWord = ['delete', 'xóa']
    preContent = content[1]
    for x in keyWord:
        print(f"Key word {x} so với {content[0]}")
        if x.upper() in content[0].upper():
            print("Thay đổi preconte")
            preContent = content[3]


    return preContent, content[3], timeStamp

async def cell_Content(page:Page,cell:str = None ):

    #Tìm Cell
    await page.press("body","Control+J")
    await page.keyboard.type(f"{cell}")
    await page.keyboard.press("Enter")

    # Click chuột phải vào ô đó
    await page.keyboard.press("Shift+F10")

    #Lấy dữ liệu
    return await getPreviusContent(page)



async def run(playwright:Playwright,user_dir: str) -> None:
    browser_context = await playwright.chromium.launch_persistent_context(
            user_data_dir= r"D:\Desktop\Playwright_profile",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            channel="chrome"   # hoặc "msedge" nếu bạn muốn Edge
        )
   
    page = await browser_context.new_page()

    await page.goto("https://docs.google.com/spreadsheets/d/1lNsIW2A1gmurYZ-DJt65xuX_yEsxyvoqPx84Q2B8rEM/edit?gid=0#gid=0")
    locator = page.get_by_role("link", name="Đăng nhập")
    if await locator.count() > 0:
        await locator.click()
        await page.wait_for_url("**/docs.google.com/**")
        

    # await cell_Content(page,"D2")
    
    preContent, newContent, timeStamp = await cell_Content(page,"D2")
    

    requirements_prev, new_req, requirements_timestamp_prev = await cell_Content(page,"D7")

    print("Previus requirement: ", requirements_prev)
    print("New requirement: " ,new_req)


    test =  {'preContent': preContent, 'timeStamp': timeStamp, 'requirements_prev':requirements_prev, 'requirements_timestamp_prev':requirements_timestamp_prev}
    # Lưu vào file JSON
    with open("data/history.json", "w", encoding="utf-8") as f:
        json.dump(test, f, ensure_ascii=False, indent=4)

    

    try:
        await page.wait_for_timeout(1000000)
    except:
        print("Manually close chrome.")

 

async def main():
    async with async_playwright() as playwright:
        await run(playwright,config["USER_DATA_DIR"])


asyncio.run(main())


