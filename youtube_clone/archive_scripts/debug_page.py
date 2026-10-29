import asyncio
from playwright.async_api import async_playwright

async def debug_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: print(f"Console [{msg.type}]: {msg.text}"))

        await page.goto("http://localhost:8000")
        await page.wait_for_timeout(2000)

        print("Total page errors:", len(errors))
        for err in errors:
            print(err)

        cards = await page.query_selector_all('.yt-video-card')
        print(f"Cards found: {len(cards)}")
        await browser.close()

asyncio.run(debug_page())
