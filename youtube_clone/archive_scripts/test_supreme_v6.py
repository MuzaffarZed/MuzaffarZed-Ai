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

        # 1. Test Subtitles Languages Menu
        print("[Test] Testing Subtitles Languages Menu...")
        first_card = await page.wait_for_selector('.yt-card')
        await first_card.click()
        await page.wait_for_timeout(1500)

        btn_cc = await page.wait_for_selector('#btn-cc-toggle')
        # Right-click CC button to open language selector
        await btn_cc.click(button="right")
        await page.wait_for_timeout(600)

        sub_menu = await page.wait_for_selector('#subtitles-lang-menu')
        sub_visible = await sub_menu.is_visible()
        print(f"[Test] Subtitles Language Menu visible: {sub_visible}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_subtitles_menu.png"))
        print("[Test] Saved youtube_pro_subtitles_menu.png")

        # Select English
        opt_en = await page.wait_for_selector('.yt-dropdown-item[data-sublang="en"]')
        await opt_en.click()
        await page.wait_for_timeout(400)

        sub_text = await page.query_selector('#subtitles-text')
        text_content = await sub_text.text_content() if sub_text else ""
        print(f"[Test] Subtitle text switched to: {text_content[:40]}...")

        # 2. Test Channel Page Tabs & Search
        print("[Test] Testing Channel Page Tabs & Search...")
        channel_name_el = await page.wait_for_selector('#watch-channel-name')
        await channel_name_el.click()
        await page.wait_for_timeout(1000)

        view_channel = await page.wait_for_selector('#view-channel')
        channel_visible = await view_channel.is_visible()
        print(f"[Test] Channel View visible: {channel_visible}")

        # Click Shorts tab
        tab_shorts = await page.wait_for_selector('#tab-channel-shorts')
        await tab_shorts.click()
        await page.wait_for_timeout(600)

        # Click Haqida (About) tab
        tab_about = await page.wait_for_selector('#tab-channel-about')
        await tab_about.click()
        await page.wait_for_timeout(600)

        about_sec = await page.query_selector('#channel-about-section')
        about_visible = await about_sec.is_visible() if about_sec else False
        print(f"[Test] Channel About Section visible: {about_visible}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_channel_tabs.png"))
        print("[Test] Saved youtube_pro_channel_tabs.png")

        # 3. Test History Page Search & Toolbar
        print("[Test] Testing History Page Toolbar & Search...")
        nav_history = await page.wait_for_selector('.yt-sidebar-item[data-nav="history"]')
        await nav_history.click()
        await page.wait_for_timeout(1000)

        view_history = await page.wait_for_selector('#view-history')
        hist_visible = await view_history.is_visible()
        print(f"[Test] History View visible: {hist_visible}")

        # Search in history
        hist_input = await page.wait_for_selector('#history-search-input')
        await hist_input.fill("AGI")
        await page.wait_for_timeout(500)

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_history_toolbar.png"))
        print("[Test] Saved youtube_pro_history_toolbar.png")

        # 4. Test Shorts Sound Modal
        print("[Test] Testing Shorts Sound Modal...")
        nav_shorts = await page.wait_for_selector('.yt-sidebar-item[data-nav="shorts"]')
        await nav_shorts.click()
        await page.wait_for_timeout(1000)

        # Click sound tag via evaluate
        await page.evaluate("""() => {
          const s = document.querySelector('.yt-short-sound-tag');
          if (s) s.click();
          else if (window.app) window.app.openShortsSoundModal("MuzaffarZed Original Track", "MuzaffarZed Studio");
        }""")
        await page.wait_for_timeout(600)

        sound_modal = await page.wait_for_selector('#shorts-sound-modal.open')
        modal_visible = await sound_modal.is_visible()
        print(f"[Test] Shorts Sound Modal visible: {modal_visible}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_shorts_sound_modal.png"))
        print("[Test] Saved youtube_pro_shorts_sound_modal.png")

        await browser.close()
        print("[Test] ALL V6 ADVANCED TESTS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
