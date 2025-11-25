import json
from playwright.async_api import Playwright, Page, async_playwright, expect
import asyncio
from dotenv import dotenv_values


config = dotenv_values(".env")

def getEmailContent() -> json:
    with open("data/basic.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    with open("data/history.json", "r", encoding="utf-8") as f:
        history = json.load(f)

    content = {'Name':data['Name']['0'],
               'Email':data['Email']['0'],
               'Subject':data['Content']['0'],
                'preContent':history['preContent'],
                'Requirement':history['requirements_prev']
               }
   
    return content

content = getEmailContent()

async def sendEmail(page: Page, content:json):
    print("send mail work")
    print(content)

    await page.wait_for_timeout(2000)
    #page.wait_for_selector(".AD", state="visible", timeout=5000)
    region = page.get_by_role("region")
    subject = region.locator('input[name="subjectbox"]').first
    to = region.get_by_role("combobox").first
    body = page.locator('div[role="textbox"]').first


    await body.fill(f"Dear {content['Name']}, \n \n \
[Content from Level 2 D2 previous version: {content['preContent']}]\
\n [Requirements from Level 2 D7 previous version: {content['Requirement']}]                    \
                    ")
    await to.fill(f"{content['Email']}")
    await subject.fill(content['Subject'])



    # :qa :pz :rf
    return

async def run(playwright:Playwright,user_dir: str) -> None:
    browser_context = await playwright.chromium.launch_persistent_context(
            user_data_dir= user_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            channel="chrome"   # hoặc "msedge" nếu bạn muốn Edge
        )
   
    page = await browser_context.new_page()

    await page.goto("https://mail.google.com/mail/u/0/#inbox?compose=new")
   
    await sendEmail(page,getEmailContent())

    try:
        await page.wait_for_timeout(1000000)
    except:
        print("Manually close chrome.")

async def main():
    async with async_playwright() as playwright:
        await run(playwright,config["USER_DATA_DIR"])

asyncio.run(main())


