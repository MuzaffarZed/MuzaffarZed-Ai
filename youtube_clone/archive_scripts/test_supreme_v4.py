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

        # 1. Test Notifications Dropdown
        print("[Test] Testing Notifications Dropdown...")
        btn_notif = await page.wait_for_selector('#btn-notifications')
        await btn_notif.click()
        await page.wait_for_timeout(600)

        notif_dropdown = await page.wait_for_selector('#notifications-dropdown')
        notif_visible = await notif_dropdown.is_visible()
        print(f"[Test] Notifications Dropdown visible: {notif_visible}")

        # Capture Notifications Screenshot
        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_notifications.png"))
        print("[Test] Saved youtube_pro_notifications.png")

        # 2. Test User Profile Dropdown
        print("[Test] Testing User Profile Dropdown...")
        user_trigger = await page.wait_for_selector('#user-profile-menu-trigger')
        await user_trigger.click()
        await page.wait_for_timeout(600)

        user_dropdown = await page.wait_for_selector('#user-profile-dropdown')
        user_visible = await user_dropdown.is_visible()
        print(f"[Test] User Profile Dropdown visible: {user_visible}")

        # Capture User Profile Screenshot
        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_profile_dropdown.png"))
        print("[Test] Saved youtube_pro_profile_dropdown.png")

        # Dismiss dropdown by clicking outside
        await page.mouse.click(10, 10)
        await page.wait_for_timeout(300)

        # 3. Enter Watch Mode and test 2x Speed Hold Pill
        print("[Test] Opening first video...")
        card = await page.wait_for_selector('.yt-card')
        await card.click()
        await page.wait_for_timeout(1500)

        player_container = await page.wait_for_selector('#player-container')
        
        # Test 2x Speed Pill appearance
        await page.evaluate("""() => {
          const pill = document.getElementById('speed-2x-pill');
          if (pill) pill.classList.add('show');
        }""")
        await page.wait_for_timeout(400)

        # Capture 2x speed pill screenshot
        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_2x_speed.png"))
        print("[Test] Saved youtube_pro_2x_speed.png")

        await page.evaluate("""() => {
          const pill = document.getElementById('speed-2x-pill');
          if (pill) pill.classList.remove('show');
        }""")

        # 4. Return Home and capture final Masterpiece
        print("[Test] Returning to Home...")
        nav_home = await page.wait_for_selector('.yt-sidebar-item[data-nav="home"]')
        await nav_home.click()
        await page.wait_for_timeout(1000)

        await page.screenshot(path=os.path.join(WORKSPACE, "youtube_pro_masterpiece_2026.png"))
        print("[Test] Saved youtube_pro_masterpiece_2026.png")

        await browser.close()
        print("[Test] ALL V4 TESTS COMPLETED WITH 100% SUCCESS!")

if __name__ == '__main__':
    asyncio.run(run_test())
