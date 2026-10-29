with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Subtitles language dropdown inside player-container
sub_menu_html = """
              <!-- Subtitle Languages Menu -->
              <div id="subtitles-lang-menu" class="yt-subtitles-menu" style="display: none;">
                <div style="font-size: 11px; font-weight: 700; color: var(--yt-text-secondary); margin-bottom: 4px; padding: 4px 8px; border-bottom: 1px solid var(--yt-border);">
                  SUBTITR TILI
                </div>
                <div class="yt-dropdown-item" data-sublang="uz">🇺🇿 O'zbekcha</div>
                <div class="yt-dropdown-item" data-sublang="en">🇬🇧 English</div>
                <div class="yt-dropdown-item" data-sublang="ru">🇷🇺 Русский</div>
                <div class="yt-dropdown-item" data-sublang="tr">🇹🇷 Türkçe</div>
                <div class="yt-dropdown-divider" style="height: 1px; background: var(--yt-border); margin: 4px 0;"></div>
                <div class="yt-dropdown-item" data-sublang="off" style="color: #ff5555;">Subtitrlarni o'chirish</div>
              </div>
"""

sub_overlay_marker = 'id="subtitles-overlay"'
pos = html.find(sub_overlay_marker)
if pos != -1 and 'id="subtitles-lang-menu"' not in html:
    div_start = html.rfind('<div id="subtitles-overlay"', 0, pos)
    html = html[:div_start] + sub_menu_html + html[div_start:]
    print("Inserted Subtitles Language Dropdown!")

# 2. Channel Page Tabs & Channel Search & Channel About Section
old_channel_tabs = """        <!-- Channel Tabs -->
        <div class="yt-channel-tabs">
          <div class="yt-channel-tab active" id="tab-channel-videos">Videolar</div>
          <div class="yt-channel-tab" id="tab-channel-about">Haqida</div>
        </div>

        <!-- Channel Videos Grid -->
        <div class="yt-video-grid" id="channel-videos-grid" style="padding-top: 20px;"></div>"""

new_channel_tabs = """        <!-- Channel Tabs & Search -->
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--yt-border);">
          <div class="yt-channel-tabs" style="border-bottom: none;">
            <div class="yt-channel-tab active" id="tab-channel-videos">Videolar</div>
            <div class="yt-channel-tab" id="tab-channel-shorts">Shorts</div>
            <div class="yt-channel-tab" id="tab-channel-playlists">Playlistlar</div>
            <div class="yt-channel-tab" id="tab-channel-about">Haqida</div>
          </div>
          <div class="yt-channel-search-box">
            <i data-lucide="search" style="width: 14px; height: 14px; color: var(--yt-text-secondary);"></i>
            <input type="text" id="channel-search-input" placeholder="Ushbu kanaldan qidirish...">
          </div>
        </div>

        <!-- Channel Videos Grid -->
        <div class="yt-video-grid" id="channel-videos-grid" style="padding-top: 20px;"></div>

        <!-- Channel About Section (Collapsible) -->
        <div id="channel-about-section" style="display: none; padding: 24px 0; max-width: 800px;">
          <h3 style="font-size: 18px; font-weight: 700; margin-bottom: 12px;">Kanal Tavsifi</h3>
          <p id="channel-about-desc" style="font-size: 14px; line-height: 1.7; color: var(--yt-text-primary); margin-bottom: 18px;">
            MuzaffarZed tomonidan yaratilgan eng ilg'or AGI texnologiyalari, neyron tarmoqlar va zamonaviy veb-arxitektura bo'yicha maxsus rasmiy media portal.
          </p>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; background: var(--yt-surface); border: 1px solid var(--yt-border); border-radius: 12px; padding: 16px; font-size: 13px;">
            <div><b>Bog'lanish:</b> muzaffar@zed.ai</div>
            <div><b>Manzil:</b> O'zbekiston, Toshkent</div>
            <div><b>Qo'shilgan sana:</b> 2026-yil 1-yanvar</div>
            <div><b>Umumiy ko'rishlar:</b> 4.8M ko'rish</div>
          </div>
        </div>"""

if old_channel_tabs in html:
    html = html.replace(old_channel_tabs, new_channel_tabs, 1)
    print("Updated Channel Page Tabs & Search!")
else:
    print("Warning: old_channel_tabs not matched exactly!")

# 3. History Page Toolbar
old_history_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h2 style="font-size: 22px; font-weight: 700;">Ko'rishlar Tarixi</h2>
          <button id="btn-clear-all-history" class="yt-btn-secondary" style="border: 1px solid var(--yt-border); color: #ff5555; display: flex; align-items: center; gap: 6px;">
            <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
            <span>Tarixni tozalash</span>
          </button>
        </div>"""

new_history_header = """        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
          <h2 style="font-size: 22px; font-weight: 700;">Ko'rishlar Tarixi</h2>
          <div class="yt-history-toolbar">
            <input type="text" id="history-search-input" placeholder="Tarixdan qidirish..." class="yt-history-search-input">
            <button id="btn-pause-history" class="yt-btn-secondary" style="font-size: 12px; display: flex; align-items: center; gap: 6px;">
              <i data-lucide="pause-circle" id="icon-pause-history" style="width: 16px; height: 16px;"></i>
              <span id="pause-history-label">Tarixni pauzalash</span>
            </button>
            <button id="btn-clear-all-history" class="yt-btn-secondary" style="border: 1px solid var(--yt-border); color: #ff5555; display: flex; align-items: center; gap: 6px;">
              <i data-lucide="trash-2" style="width: 16px; height: 16px;"></i>
              <span>Tarixni tozalash</span>
            </button>
          </div>
        </div>"""

if old_history_header in html:
    html = html.replace(old_history_header, new_history_header, 1)
    print("Updated History Page Toolbar!")
else:
    print("Warning: old_history_header not matched exactly!")

# 4. Shorts Sound Modal
sound_modal_html = """
  <!-- Shorts Sound Modal -->
  <div class="yt-modal-backdrop" id="shorts-sound-modal">
    <div class="yt-modal-card" style="max-width: 400px; text-align: center;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 17px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
          <i data-lucide="music" style="width: 20px; height: 20px; color: var(--yt-red);"></i>
          <span>Audio Trek Ma'lumoti</span>
        </h3>
        <button class="yt-icon-btn" id="btn-close-sound-modal">
          <i data-lucide="x" style="width: 18px; height: 18px;"></i>
        </button>
      </div>
      <div style="margin: 16px 0;">
        <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #ff007f, #7928ca); margin: 0 auto 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(255,0,128,0.4);">
          <i data-lucide="disc" style="width: 36px; height: 36px; color: white;"></i>
        </div>
        <h4 id="sound-modal-title" style="font-size: 16px; font-weight: 700;">Original Audio</h4>
        <p id="sound-modal-author" style="font-size: 13px; color: var(--yt-text-secondary); margin-top: 4px;">MuzaffarZed Studio</p>
      </div>
      <button id="btn-use-sound" class="yt-btn-primary" style="width: 100%; padding: 10px; font-weight: 700; margin-top: 8px;">
        Ushbu audiodan foydalanish
      </button>
    </div>
  </div>
"""

body_end = "</body>"
pos_b = html.rfind(body_end)
if pos_b != -1 and 'id="shorts-sound-modal"' not in html:
    html = html[:pos_b] + sound_modal_html + html[pos_b:]
    print("Inserted Shorts Sound Modal!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("patch_html_v6.py complete!")
