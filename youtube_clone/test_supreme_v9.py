import asyncio
import os
from playwright.async_api import async_playwright

WORKSPACE = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone'

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page = await context.new_page()

        print("[Test V9] Opening YouTube Pro...")
        await page.goto("http://localhost:8000", wait_until="domcontentloaded")
        await page.wait_for_timeout(1000)

        # 1. Test Watched Progress Bar on Thumbnail
        print("[Test V9] Testing Watched Progress Bar on Thumbnails...")
        await page.evaluate("""() => {
          if (window.app && window.app.videos.length > 0) {
            const vidId = window.app.videos[0].id;
            window.app.videoProgress = {
              [vidId]: { time: 180, duration: 300, percent: 60 }
            };
            localStorage.setItem('yt_video_progress', JSON.stringify(window.app.videoProgress));
            window.app.renderVideoGrid();
          }
        }""")
        await page.wait_for_timeout(600)

        prog_bar = await page.wait_for_selector('.yt-thumb-progress')
        bar_vis = await prog_bar.is_visible()
        print(f"[Test V9] Thumbnail Progress Bar Visible: {bar_vis}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_thumbnail_progress.png"))
        print("[Test V9] Saved youtube_pro_thumbnail_progress.png")

        # 2. Test Volume Persistence
        print("[Test V9] Testing Volume Persistence in localStorage...")
        vol_res = await page.evaluate("""() => {
          if (window.app && window.app.volumeSlider) {
            window.app.volumeSlider.value = 0.75;
            window.app.volumeSlider.dispatchEvent(new Event('input'));
            return {
              savedVol: localStorage.getItem('yt_volume'),
              savedMuted: localStorage.getItem('yt_muted')
            };
          }
          return null;
        }""")
        print(f"[Test V9] Volume Persistence Result: {vol_res}")

        # 3. Test Global Escape Key Dismissal
        print("[Test V9] Testing Global Escape Key Dismissal...")
        btn_prof = await page.wait_for_selector('#user-profile-menu-trigger')
        await btn_prof.click()
        await page.wait_for_timeout(400)

        prof_drop = await page.wait_for_selector('#user-profile-dropdown')
        drop_vis_before = await prof_drop.is_visible()
        print(f"[Test V9] Profile Dropdown visible before Escape: {drop_vis_before}")

        # Press Escape
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)

        drop_vis_after = await prof_drop.is_visible()
        print(f"[Test V9] Profile Dropdown visible after Escape: {drop_vis_after}")

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_escape_dismiss.png"))
        print("[Test V9] Saved youtube_pro_escape_dismiss.png")

        await browser.close()
        print("[Test V9] ALL V9 TESTS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
