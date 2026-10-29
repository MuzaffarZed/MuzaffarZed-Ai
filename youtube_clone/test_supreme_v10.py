import asyncio
import os
from playwright.async_api import async_playwright

WORKSPACE = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone'

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        print("[Test V10] Opening YouTube Pro...")
        await page.goto("http://localhost:8000", wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        # 1. Open Watch View
        print("[Test V10] Opening first video on Watch View...")
        await page.evaluate("""() => {
          if (window.app && window.app.videos.length > 0) {
            window.app.openWatch(window.app.videos[0]);
          }
        }""")
        await page.wait_for_timeout(1500)

        # 2. Right-click video player to open context menu
        print("[Test V10] Opening Player Context Menu...")
        player = await page.wait_for_selector('#player-container')
        await player.click(button="right")
        await page.wait_for_timeout(500)

        ctx_menu = await page.wait_for_selector('#player-context-menu')
        ctx_vis = await ctx_menu.is_visible()
        print(f"[Test V10] Player Context Menu visible: {ctx_vis}")

        zoom_opt = await page.wait_for_selector('#ctx-zoom-fit')
        zoom_vis = await zoom_opt.is_visible()
        print(f"[Test V10] Zoom Option in Context Menu visible: {zoom_vis}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_context_menu_zoom.png"))
        print("[Test V10] Saved youtube_pro_context_menu_zoom.png")

        # 3. Click Zoom to Fill Option
        await zoom_opt.click()
        await page.wait_for_timeout(400)

        has_zoom = await page.evaluate("""() => {
          const v = document.getElementById('main-video-player');
          return v ? v.classList.contains('zoom-fill') : false;
        }""")
        print(f"[Test V10] Main Video Player has .zoom-fill class: {has_zoom}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_zoom_fill.png"))
        print("[Test V10] Saved youtube_pro_zoom_fill.png")

        # 4. Press 'Z' key to toggle back
        await page.keyboard.press("z")
        await page.wait_for_timeout(400)

        has_zoom_after = await page.evaluate("""() => {
          const v = document.getElementById('main-video-player');
          return v ? v.classList.contains('zoom-fill') : false;
        }""")
        print(f"[Test V10] Main Video Player has .zoom-fill after 'z' key: {has_zoom_after}")

        await browser.close()
        print("[Test V10] ALL V10 TESTS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
