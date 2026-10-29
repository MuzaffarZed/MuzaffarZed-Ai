with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Scrub Bar update
old_scrub = """                <!-- Scrub Bar -->
                <div class="yt-scrub-bar" id="scrub-bar">
                  <div class="yt-scrub-fill" id="scrub-fill">
                    <div class="yt-scrub-handle"></div>
                  </div>
                </div>"""

new_scrub = """                <!-- Scrub Bar -->
                <div class="yt-scrub-bar" id="scrub-bar">
                  <div class="yt-scrub-buffer" id="scrub-buffer"></div>
                  <div class="yt-scrub-fill" id="scrub-fill">
                    <div class="yt-scrub-handle"></div>
                  </div>
                  <div class="yt-scrub-tooltip" id="scrub-tooltip" style="display: none;">
                    <span class="yt-tooltip-chapter" id="tooltip-chapter">Mundarija</span>
                    <span class="yt-tooltip-time" id="tooltip-time">0:00</span>
                  </div>
                </div>"""

# 2. Center Splash inside player-container (place after subtitles-overlay)
old_subtitles = """              <!-- Subtitle Overlay -->
              <div id="subtitles-overlay" class="yt-subtitles-overlay" style="display: none;">
                <span id="subtitles-text">Avtomatik subtitrlar faol</span>
              </div>"""

new_subtitles_and_splash = """              <!-- Subtitle Overlay -->
              <div id="subtitles-overlay" class="yt-subtitles-overlay" style="display: none;">
                <span id="subtitles-text">Avtomatik subtitrlar faol</span>
              </div>

              <!-- Center Play/Pause Splash HUD -->
              <div id="player-center-splash" class="yt-center-splash">
                <i data-lucide="play" id="center-splash-icon" style="width: 38px; height: 38px; color: white;"></i>
              </div>"""

# 3. Chapters button in action pills (after btn-ai-summary)
old_ai_btn = """                <!-- AI Summary Button -->
                <button class="yt-pill-btn" id="btn-ai-summary" style="background: linear-gradient(135deg, rgba(255,0,128,0.2), rgba(0,180,255,0.2)); border: 1px solid rgba(255,255,255,0.2);">
                  <i data-lucide="sparkles" style="width: 18px; height: 18px; color: #3ea6ff;"></i>
                  <span style="font-weight: 700; color: #3ea6ff;">AI Xulosa</span>
                </button>"""

new_ai_and_chapters = """                <!-- AI Summary Button -->
                <button class="yt-pill-btn" id="btn-ai-summary" style="background: linear-gradient(135deg, rgba(255,0,128,0.2), rgba(0,180,255,0.2)); border: 1px solid rgba(255,255,255,0.2);">
                  <i data-lucide="sparkles" style="width: 18px; height: 18px; color: #3ea6ff;"></i>
                  <span style="font-weight: 700; color: #3ea6ff;">AI Xulosa</span>
                </button>

                <!-- Chapters Button -->
                <button class="yt-pill-btn" id="btn-chapters" title="Video mundarijasi (Chapters)">
                  <i data-lucide="layers" style="width: 18px; height: 18px; color: var(--yt-blue);"></i>
                  <span>Mundarija</span>
                </button>"""

# 4. Comments sort button ID
old_sort_btn = """                <button class="yt-btn-secondary" style="display: flex; align-items: center; gap: 8px;">
                  <i data-lucide="arrow-down-up" style="width: 16px; height: 16px;"></i>
                  <span>Tartiblash</span>
                </button>"""

new_sort_btn = """                <button class="yt-btn-secondary" id="btn-sort-comments" style="display: flex; align-items: center; gap: 8px;">
                  <i data-lucide="arrow-down-up" style="width: 16px; height: 16px;"></i>
                  <span id="sort-comments-label">Eng saralar</span>
                </button>"""

# 5. Shorts comments drawer inside view-shorts
old_shorts_view = """      <!-- View 3: Shorts View -->
      <section id="view-shorts" style="display: none; height: 100%;">
        <div class="yt-shorts-container" id="shorts-container">
          <!-- Dynamically populated short reels -->
        </div>
      </section>"""

new_shorts_view = """      <!-- View 3: Shorts View -->
      <section id="view-shorts" style="display: none; height: 100%;">
        <div class="yt-shorts-container" id="shorts-container">
          <!-- Dynamically populated short reels -->
        </div>

        <!-- Shorts Comments Drawer -->
        <div class="yt-shorts-comments-drawer" id="shorts-comments-drawer" style="display: none;">
          <div class="yt-shorts-drawer-header">
            <div style="font-weight: 700; font-size: 15px; display: flex; align-items: center; gap: 8px;">
              <span>Fikrlar</span>
              <span id="shorts-comments-count" style="font-size: 13px; color: var(--yt-text-secondary);">(0)</span>
            </div>
            <button class="yt-icon-btn" id="btn-close-shorts-comments" style="width: 28px; height: 28px;">
              <i data-lucide="x" style="width: 16px; height: 16px;"></i>
            </button>
          </div>
          <div class="yt-shorts-drawer-list" id="shorts-comments-list"></div>
          <div class="yt-shorts-drawer-input-row">
            <input type="text" id="shorts-comment-input" placeholder="Izoh qoldiring..." style="flex: 1; background: var(--yt-surface); border: 1px solid var(--yt-border); border-radius: 20px; padding: 8px 14px; font-size: 13px; color: #fff; outline: none;">
            <button id="btn-submit-shorts-comment" class="yt-btn-primary" style="padding: 6px 14px; font-size: 13px;">Yuborish</button>
          </div>
        </div>
      </section>"""

# 6. Chapters Modal and Player Context Menu before </body>
modals_insert = """
  <!-- Video Chapters Modal -->
  <div class="yt-modal-backdrop" id="chapters-modal">
    <div class="yt-modal-card" style="max-width: 440px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="font-size: 18px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
          <i data-lucide="layers" style="width: 20px; height: 20px; color: var(--yt-blue);"></i>
          <span>Video Mundarijasi (Chapters)</span>
        </h3>
        <button class="yt-icon-btn" id="btn-close-chapters-modal">
          <i data-lucide="x" style="width: 20px; height: 20px;"></i>
        </button>
      </div>
      <div id="chapters-list-container" style="display: flex; flex-direction: column; gap: 8px; max-height: 360px; overflow-y: auto;">
        <!-- Dynamically generated chapter rows -->
      </div>
    </div>
  </div>

  <!-- Custom Video Player Context Menu -->
  <div id="player-context-menu" class="yt-context-menu" style="display: none;">
    <div class="yt-dropdown-item" id="ctx-loop">
      <i data-lucide="repeat" style="width: 16px; height: 16px;"></i>
      <span id="ctx-loop-text">Videoni takrorlash (Loop)</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-copy-url">
      <i data-lucide="link" style="width: 16px; height: 16px;"></i>
      <span>Video havolasini nusxalash</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-copy-time">
      <i data-lucide="clock" style="width: 16px; height: 16px;"></i>
      <span>Hozirgi vaqt bilan nusxalash</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-copy-embed">
      <i data-lucide="code" style="width: 16px; height: 16px;"></i>
      <span>Embed kodini nusxalash</span>
    </div>
    <div class="yt-context-divider"></div>
    <div class="yt-dropdown-item" id="ctx-stats">
      <i data-lucide="info" style="width: 16px; height: 16px;"></i>
      <span>Texnik statistika (Stats for nerds)</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-eq">
      <i data-lucide="sliders" style="width: 16px; height: 16px;"></i>
      <span>Studio Ekvalayzer (EQ)</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-pip">
      <i data-lucide="picture-in-picture-2" style="width: 16px; height: 16px;"></i>
      <span>Picture-in-Picture</span>
    </div>
  </div>
"""

# Apply replacements
replacements = [
    (old_scrub, new_scrub, "Scrub Bar"),
    (old_subtitles, new_subtitles_and_splash, "Center Splash"),
    (old_ai_btn, new_ai_and_chapters, "Chapters Button"),
    (old_sort_btn, new_sort_btn, "Sort Comments Button"),
    (old_shorts_view, new_shorts_view, "Shorts Drawer")
]

modified = html
for old_s, new_s, label in replacements:
    if old_s in modified:
        modified = modified.replace(old_s, new_s, 1)
        print(f"Replaced {label} successfully!")
    else:
        print(f"Warning: {label} target not found exactly!")

if "id=\"chapters-modal\"" not in modified:
    body_idx = modified.rfind("</body>")
    if body_idx != -1:
        modified = modified[:body_idx] + modals_insert + modified[body_idx:]
        print("Inserted chapters-modal & player-context-menu successfully!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'w', encoding='utf-8') as f:
    f.write(modified)

print("index.html patch completed!")
