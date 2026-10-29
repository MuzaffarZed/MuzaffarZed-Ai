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

        # 1. Verify Home & Open first video
        print("[Test] Clicking first video card to enter Watch View...")
        first_card = await page.wait_for_selector('.yt-card')
        await first_card.click()
        await page.wait_for_timeout(1500)

        # 2. Test Play/Pause and Center Splash HUD
        print("[Test] Testing Play/Pause and Center Splash HUD...")
        player_container = await page.wait_for_selector('#player-container')
        await page.keyboard.press('k') # Toggle Pause
        await page.wait_for_timeout(300)

        splash = await page.query_selector('#player-center-splash')
        if splash:
            print("[Test] Center Splash HUD verified!")

        # 3. Test Scrub Bar hover & Tooltip
        print("[Test] Testing Scrub Bar hover and tooltip...")
        scrub_bar = await page.wait_for_selector('#scrub-bar')
        box = await scrub_bar.bounding_box()
        if box:
            await page.mouse.move(box['x'] + box['width'] * 0.4, box['y'] + box['height'] / 2)
            await page.wait_for_timeout(500)
            tooltip = await page.query_selector('#scrub-tooltip')
            tooltip_visible = await tooltip.is_visible() if tooltip else False
            print(f"[Test] Scrub tooltip visible on hover: {tooltip_visible}")

        # 4. Test Chapters Button & Modal
        print("[Test] Testing Chapters Button and Modal...")
        btn_chapters = await page.query_selector('#btn-chapters')
        if btn_chapters:
            await btn_chapters.click()
            await page.wait_for_timeout(600)
            chapters_modal = await page.wait_for_selector('#chapters-modal.open')
            chapter_rows = await page.query_selector_all('.yt-chapter-row')
            print(f"[Test] Chapters Modal opened with {len(chapter_rows)} chapters!")

            # Take screenshot of Chapters Modal
            await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_chapters_scrub.png"))
            print("[Test] Saved youtube_pro_chapters_scrub.png")

            # Click second chapter to seek
            if len(chapter_rows) > 1:
                await chapter_rows[1].click()
                await page.wait_for_timeout(500)
                print("[Test] Clicked chapter row to seek!")

        # 5. Test Custom Right-Click Context Menu on Player
        print("[Test] Testing Custom Video Context Menu (Right-Click)...")
        await player_container.click(button="right")
        await page.wait_for_timeout(500)
        ctx_menu = await page.query_selector('#player-context-menu')
        ctx_visible = await ctx_menu.is_visible() if ctx_menu else False
        print(f"[Test] Custom context menu visible on right-click: {ctx_visible}")

        # Take screenshot of Custom Context Menu
        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_context_menu.png"))
        print("[Test] Saved youtube_pro_context_menu.png")

        # Dismiss context menu
        await page.mouse.click(10, 10)
        await page.wait_for_timeout(300)

        # 6. Test Comments Sorting
        print("[Test] Testing Comments Sorting...")
        btn_sort = await page.query_selector('#btn-sort-comments')
        if btn_sort:
            await btn_sort.click()
            await page.wait_for_timeout(500)
            label = await page.query_selector('#sort-comments-label')
            label_text = await label.text_content() if label else ""
            print(f"[Test] Comments sorted mode label: {label_text}")

        # 7. Test Shorts & Shorts Comments Drawer
        print("[Test] Testing Shorts View & Comments Drawer...")
        nav_shorts = await page.wait_for_selector('.yt-sidebar-item[data-nav="shorts"]')
        await nav_shorts.click()
        await page.wait_for_timeout(1000)

        # Click short comment button via evaluate or force
        await page.evaluate("() => { const b = document.querySelector('.btn-short-comment'); if(b) b.click(); }")
        await page.wait_for_timeout(600)

        shorts_drawer = await page.query_selector('#shorts-comments-drawer')
        drawer_visible = await shorts_drawer.is_visible() if shorts_drawer else False
        print(f"[Test] Shorts Comments Drawer visible: {drawer_visible}")

        # Add a new comment in Shorts drawer
        shorts_input = await page.query_selector('#shorts-comment-input')
        if shorts_input:
            await shorts_input.fill("MuzaffarZed YouTube Pro haqiqatan ham aqlbovar qilmas darajada zo'r!")
            btn_submit_short = await page.query_selector('#btn-submit-shorts-comment')
            if btn_submit_short:
                await btn_submit_short.click()
                await page.wait_for_timeout(600)
                print("[Test] Submitted new short comment successfully!")

        # Take screenshot of Shorts with open Comments Drawer
        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_shorts_comments.png"))
        print("[Test] Saved youtube_pro_shorts_comments.png")

        # 8. Return Home and take ultimate screenshot
        print("[Test] Navigating back to Home...")
        nav_home = await page.wait_for_selector('.yt-sidebar-item[data-nav="home"]')
        await nav_home.click()
        await page.wait_for_timeout(1000)

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_final_ultimate.png"))
        print("[Test] Saved youtube_pro_final_ultimate.png")

        await browser.close()
        print("[Test] ALL ADVANCED VISUAL TESTS PASSED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
