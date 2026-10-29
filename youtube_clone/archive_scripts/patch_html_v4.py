with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 2x Speed Pill inside player-container
speed_pill = """
              <!-- 2x Speed Hold Pill -->
              <div id="speed-2x-pill" class="yt-speed-2x-pill">
                <span class="pill-indicator">▶▶</span>
                <span>2x Tezlik</span>
              </div>
"""

splash_marker = 'id="player-center-splash" class="yt-center-splash">'
pos = html.find(splash_marker)
if pos != -1 and "id=\"speed-2x-pill\"" not in html:
    # insert before center splash
    splash_div_start = html.rfind('<div id="player-center-splash"', 0, pos)
    html = html[:splash_div_start] + speed_pill + html[splash_div_start:]
    print("Inserted 2x Speed Pill!")

# 2. Notifications & User profile dropdowns right after </header>
header_end = "</header>"
dropdowns_html = """
  <!-- Notifications Dropdown -->
  <div id="notifications-dropdown" class="yt-notifications-dropdown" style="display: none;">
    <div class="yt-notif-header">
      <span>Bildirishnomalar</span>
      <button class="yt-icon-btn" id="btn-close-notif" style="width: 28px; height: 28px;">
        <i data-lucide="x" style="width: 16px; height: 16px;"></i>
      </button>
    </div>
    <div class="yt-notif-list" id="notif-list">
      <div class="yt-notif-item unread" data-vid="v-ai-agi-2026">
        <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80" class="yt-notif-avatar" alt="MuzaffarZed">
        <div class="yt-notif-body">
          <b>MuzaffarZed Tech</b> yangi video yukladi: <i>AGI va Sun'iy Intellektning Yangi Davri</i>
          <div class="yt-notif-time">2 soat oldin</div>
        </div>
        <img src="https://images.unsplash.com/photo-1677442136019-21780efad99a?w=800&auto=format&fit=crop&q=80" class="yt-notif-thumb" alt="Thumb">
      </div>
      <div class="yt-notif-item unread" data-vid="v-web-dev-pro">
        <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80" class="yt-notif-avatar" alt="Web Dev">
        <div class="yt-notif-body">
          <b>Web Dev Pro</b> yangi masterklass chiqardi: <i>10 daqiqada To'liq Stack Web Ilova</i>
          <div class="yt-notif-time">5 soat oldin</div>
        </div>
        <img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80" class="yt-notif-thumb" alt="Thumb">
      </div>
      <div class="yt-notif-item" data-vid="v-sci-fi-cinema">
        <img src="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80" class="yt-notif-avatar" alt="Cinema">
        <div class="yt-notif-body">
          <b>Cosmic Cosmos</b> yangi 4K film qo'shdi: <i>Qora Tuynuklar va Vaqt Nisbiyligi</i>
          <div class="yt-notif-time">Kecha</div>
        </div>
        <img src="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop&q=80" class="yt-notif-thumb" alt="Thumb">
      </div>
      <div class="yt-notif-item" data-vid="v-lofi-chill-beats">
        <img src="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80" class="yt-notif-avatar" alt="Lofi">
        <div class="yt-notif-body">
          <b>Lofi Dreamer</b> jonli oqim boshladi: <i>Dasturlash va Diqqat Uchun Chill Beats</i>
          <div class="yt-notif-time">2 kun oldin</div>
        </div>
        <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=800&auto=format&fit=crop&q=80" class="yt-notif-thumb" alt="Thumb">
      </div>
    </div>
  </div>

  <!-- User Profile / Account Menu Card -->
  <div id="user-profile-dropdown" class="yt-user-dropdown" style="display: none;">
    <div class="yt-user-header">
      <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80" alt="MuzaffarZed">
      <div>
        <div class="yt-user-name">MuzaffarZed</div>
        <div class="yt-user-handle">@muzaffarzed • Bosh Arxitektor</div>
        <span class="yt-user-badge">YouTube Pro Premium ✓</span>
      </div>
    </div>
    <div class="yt-user-menu-item" id="menu-my-channel">
      <i data-lucide="user" style="width: 18px; height: 18px;"></i>
      <span>Mening kanalim</span>
    </div>
    <div class="yt-user-menu-item" id="menu-studio">
      <i data-lucide="video" style="width: 18px; height: 18px;"></i>
      <span>MuzaffarZed Studio</span>
    </div>
    <div class="yt-user-menu-item" id="menu-premium-perks">
      <i data-lucide="sparkles" style="width: 18px; height: 18px; color: #ff007f;"></i>
      <span>Premium afzalliklari (No-Ads, 4K, EQ)</span>
    </div>
    <div class="yt-user-menu-divider"></div>
    <div class="yt-user-menu-item" id="menu-switch-theme">
      <i data-lucide="moon" style="width: 18px; height: 18px;"></i>
      <span>Mavzuni almashtirish</span>
    </div>
    <div class="yt-user-menu-item" id="menu-switch-lang">
      <i data-lucide="globe" style="width: 18px; height: 18px;"></i>
      <span>Til: O'zbekcha (UZ)</span>
    </div>
    <div class="yt-user-menu-divider"></div>
    <div class="yt-user-menu-item" id="menu-shortcuts">
      <i data-lucide="keyboard" style="width: 18px; height: 18px;"></i>
      <span>Tezkor tugmalar (?)</span>
    </div>
    <div class="yt-user-menu-item" id="menu-signout" style="color: #ff5555;">
      <i data-lucide="log-out" style="width: 18px; height: 18px;"></i>
      <span>Chiqish</span>
    </div>
  </div>
"""

pos_h = html.find(header_end)
if pos_h != -1 and "id=\"notifications-dropdown\"" not in html:
    html = html[:pos_h + len(header_end)] + dropdowns_html + html[pos_h + len(header_end):]
    print("Inserted Notifications & Profile Dropdowns!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html v4 patch complete!")
