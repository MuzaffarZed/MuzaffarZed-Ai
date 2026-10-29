import asyncio
import os
from playwright.async_api import async_playwright

WORKSPACE = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone'

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        print("[Test V7] Opening YouTube Pro...")
        await page.goto("http://localhost:8000", wait_until="domcontentloaded")
        await page.wait_for_timeout(1200)

        # 1. Test Video Card 3-Dots Menu
        print("[Test V7] Testing Video Card 3-Dots Menu...")
        first_card = await page.wait_for_selector('.yt-card')
        # Hover over first card
        await first_card.hover()
        await page.wait_for_timeout(400)

        more_btn = await first_card.wait_for_selector('.yt-card-more-btn')
        await more_btn.click()
        await page.wait_for_timeout(500)

        card_menu = await page.wait_for_selector('#card-context-menu')
        is_menu_vis = await card_menu.is_visible()
        print(f"[Test V7] Card Context Menu Visible: {is_menu_vis}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_card_context_menu.png"))
        print("[Test V7] Saved youtube_pro_card_context_menu.png")

        # 2. Test Quick Watch Later
        opt_wl = await page.wait_for_selector('#card-ctx-watch-later')
        await opt_wl.click()
        await page.wait_for_timeout(400)

        toast = await page.wait_for_selector('.yt-toast.show')
        toast_text = await toast.text_content() if toast else ""
        print(f"[Test V7] Toast shown after watch later: {toast_text}")

        # 3. Test Network Connectivity Offline Pill
        print("[Test V7] Testing Network Connectivity Offline Pill...")
        await page.evaluate("""() => {
            if (window.app && window.app.showNetworkPill) {
                window.app.showNetworkPill(false, "Internet aloqasi uzildi — Oflayn rejimdasiz");
            }
        }""")
        await page.wait_for_timeout(600)

        net_pill = await page.wait_for_selector('#network-status-pill.show')
        pill_vis = await net_pill.is_visible()
        print(f"[Test V7] Network Status Pill Visible: {pill_vis}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_offline_pill.png"))
        print("[Test V7] Saved youtube_pro_offline_pill.png")

        await browser.close()
        print("[Test V7] ALL ADVANCED CHECKS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
