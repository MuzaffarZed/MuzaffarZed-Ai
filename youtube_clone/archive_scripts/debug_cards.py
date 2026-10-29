import asyncio
from playwright.async_api import async_playwright

async def debug_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://localhost:8000")
        await page.wait_for_timeout(1000)

        cards = await page.query_selector_all('.yt-card')
        print(f"Cards found with .yt-card: {len(cards)}")
        await browser.close()

asyncio.run(debug_page())
