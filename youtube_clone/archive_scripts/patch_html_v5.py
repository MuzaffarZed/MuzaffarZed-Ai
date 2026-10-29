with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Sleep timer dropdown after Notifications dropdown
sleep_dropdown_html = """
  <!-- Sleep Timer Presets Dropdown -->
  <div id="sleep-timer-dropdown" class="yt-sleep-dropdown" style="display: none;">
    <div style="font-size: 11px; font-weight: 700; color: var(--yt-text-secondary); padding: 6px 10px; border-bottom: 1px solid var(--yt-border); margin-bottom: 4px;">
      UXLATISH TAYMERI
    </div>
    <div class="yt-dropdown-item" data-timer="10">⏱️ 10 daqiqa</div>
    <div class="yt-dropdown-item" data-timer="15">⏱️ 15 daqiqa</div>
    <div class="yt-dropdown-item" data-timer="30">⏱️ 30 daqiqa</div>
    <div class="yt-dropdown-item" data-timer="45">⏱️ 45 daqiqa</div>
    <div class="yt-dropdown-item" data-timer="60">⏱️ 60 daqiqa (1 soat)</div>
    <div class="yt-dropdown-item" data-timer="end">🎬 Video tugaganda</div>
    <div class="yt-dropdown-divider" style="height: 1px; background: var(--yt-border); margin: 4px 0;"></div>
    <div class="yt-dropdown-item" data-timer="0" style="color: #ff5555;">❌ Taymerni bekor qilish</div>
  </div>
"""

notif_marker = 'id="notifications-dropdown"'
pos = html.find(notif_marker)
if pos != -1 and 'id="sleep-timer-dropdown"' not in html:
    div_start = html.rfind('<div id="notifications-dropdown"', 0, pos)
    html = html[:div_start] + sleep_dropdown_html + html[div_start:]
    print("Inserted Sleep Timer Dropdown!")

# 2. Add View 7: Subscriptions Dedicated Feed inside main before </main>
subs_view_html = """
      <!-- View 7: Subscriptions Dedicated Feed -->
      <section id="view-subscriptions" style="display: none; padding: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <h2 style="font-size: 22px; font-weight: 800;">Obunalar Tasmasi</h2>
          <button id="btn-manage-subs-page" class="yt-btn-secondary" style="font-size: 13px; font-weight: 600; color: var(--yt-blue); display: flex; align-items: center; gap: 6px;">
            <i data-lucide="settings" style="width: 16px; height: 16px;"></i>
            <span>Obunalarni boshqarish</span>
          </button>
        </div>

        <!-- Channels Carousel Row -->
        <div class="yt-subs-channels-row" id="subs-channels-row">
          <!-- Dynamically populated subscribed channel avatars -->
        </div>

        <!-- Subscriptions Filter Chips -->
        <div style="display: flex; gap: 8px; margin: 18px 0 16px;" id="subs-filter-chips">
          <button class="yt-chip active" data-subfilter="all">Barchasi</button>
          <button class="yt-chip" data-subfilter="today">Bugun</button>
          <button class="yt-chip" data-subfilter="unwatched">Ko'rilmaganlar</button>
          <button class="yt-chip" data-subfilter="live">Jonli efir</button>
        </div>

        <!-- Subscriptions Video Grid -->
        <div class="yt-video-grid" id="subs-video-grid">
          <!-- Video cards from subscribed channels -->
        </div>
      </section>
"""

main_end = "</main>"
pos_main = html.find(main_end)
if pos_main != -1 and 'id="view-subscriptions"' not in html:
    html = html[:pos_main] + subs_view_html + html[pos_main:]
    print("Inserted Subscriptions View!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("patch_html_v5.py completed!")
