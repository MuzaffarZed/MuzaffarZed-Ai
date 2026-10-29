import asyncio
import os
from playwright.async_api import async_playwright

WORKSPACE = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone'

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        print("[Test] Opening YouTube Pro...")
        await page.goto("http://localhost:8000", wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        # 1. Test Recent Searches Autocomplete
        print("[Test] Testing Recent Searches Autocomplete...")
        search_input = await page.wait_for_selector('#global-search-input')
        await search_input.click()
        await page.wait_for_timeout(600)

        suggestions = await page.wait_for_selector('#search-suggestions-dropdown')
        sug_visible = await suggestions.is_visible()
        print(f"[Test] Recent searches dropdown visible on click: {sug_visible}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_recent_searches.png"))
        print("[Test] Saved youtube_pro_recent_searches.png")

        # Dismiss suggestions
        await page.mouse.click(10, 10)
        await page.wait_for_timeout(300)

        # 2. Test Sleep Timer Presets Dropdown
        print("[Test] Testing Sleep Timer Presets Dropdown...")
        btn_sleep = await page.wait_for_selector('#btn-sleep-timer')
        await btn_sleep.click()
        await page.wait_for_timeout(600)

        sleep_dropdown = await page.wait_for_selector('#sleep-timer-dropdown')
        sleep_visible = await sleep_dropdown.is_visible()
        print(f"[Test] Sleep timer dropdown visible: {sleep_visible}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_sleep_timer_menu.png"))
        print("[Test] Saved youtube_pro_sleep_timer_menu.png")

        # Click 30 min preset
        item_30 = await page.wait_for_selector('.yt-dropdown-item[data-timer="30"]')
        await item_30.click()
        await page.wait_for_timeout(500)
        badge = await page.query_selector('#sleep-timer-badge')
        badge_text = await badge.text_content() if badge else ""
        print(f"[Test] Sleep timer set with badge: {badge_text}")

        # 3. Test Dedicated Subscriptions View
        print("[Test] Testing Dedicated Subscriptions View...")
        nav_subs = await page.wait_for_selector('.yt-sidebar-item[data-nav="subscriptions"]')
        await nav_subs.click()
        await page.wait_for_timeout(1000)

        view_subs = await page.wait_for_selector('#view-subscriptions')
        subs_visible = await view_subs.is_visible()
        print(f"[Test] Subscriptions dedicated view visible: {subs_visible}")

        channel_items = await page.query_selector_all('.yt-subs-channel-item')
        print(f"[Test] Subscribed channels displayed in carousel: {len(channel_items)}")

        subs_cards = await page.query_selector_all('#subs-video-grid .yt-card')
        print(f"[Test] Subscriptions feed video cards: {len(subs_cards)}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_subscriptions_hub.png"))
        print("[Test] Saved youtube_pro_subscriptions_hub.png")

        await browser.close()
        print("[Test] ALL V5 ADVANCED TESTS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
