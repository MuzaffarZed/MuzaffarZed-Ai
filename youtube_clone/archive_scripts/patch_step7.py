import os

# 1. Update index.html
index_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html_content = f.read().replace('\r\n', '\n')

html_to_add = """  <!-- Video Card Context Menu (3-dots popover) -->
  <div id="card-context-menu" class="yt-context-menu" style="display: none; position: fixed; z-index: 1000;">
    <div class="yt-dropdown-item" id="card-ctx-watch-later">
      <i data-lucide="clock" style="width: 16px; height: 16px;"></i>
      <span>Keyinroq ko'rishga saqlash</span>
    </div>
    <div class="yt-dropdown-item" id="card-ctx-playlist">
      <i data-lucide="list-plus" style="width: 16px; height: 16px;"></i>
      <span>Ijro ro'yxatiga qo'shish</span>
    </div>
    <div class="yt-dropdown-item" id="card-ctx-copy-link">
      <i data-lucide="link" style="width: 16px; height: 16px;"></i>
      <span>Video havolasini nusxalash</span>
    </div>
    <div class="yt-dropdown-divider" style="height: 1px; background: var(--yt-border); margin: 4px 0;"></div>
    <div class="yt-dropdown-item" id="card-ctx-hide" style="color: #ff5555;">
      <i data-lucide="eye-off" style="width: 16px; height: 16px;"></i>
      <span>Qiziq emas (Yashirish)</span>
    </div>
  </div>

  <!-- Network Connectivity Status Pill -->
  <div id="network-status-pill" class="yt-network-status-pill">
    <span class="net-status-dot"></span>
    <span id="net-status-text">Oflayn rejim</span>
  </div>
"""

target_html = '</body>\n</html>'
if target_html in html_content:
    html_content = html_content.replace(target_html, html_to_add + '\n' + target_html)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("SUCCESS: index.html updated with card context menu and network status pill")
else:
    print("FAILED: Target not found in index.html")

# 2. Update styles.css
css_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read().replace('\r\n', '\n')

css_to_add = """
/* ----------------------------------------------------
   VIDEO CARD 3-DOTS, QUICK HOVER & NETWORK PILL
----------------------------------------------------- */

.yt-card-more-btn {
  background: transparent;
  border: none;
  color: var(--yt-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease, background-color 0.2s ease, color 0.2s ease;
  flex-shrink: 0;
  align-self: flex-start;
}

.yt-card:hover .yt-card-more-btn {
  opacity: 1;
}

.yt-card-more-btn:hover {
  background: var(--yt-surface-hover);
  color: var(--yt-text-primary);
}

.yt-thumb-quick-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: 10;
}

.yt-card:hover .yt-thumb-quick-actions {
  opacity: 1;
}

.yt-thumb-quick-btn {
  background: rgba(15, 15, 15, 0.85);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.15s ease;
}

.yt-thumb-quick-btn:hover {
  background: var(--yt-red);
  transform: scale(1.08);
}

/* Network Connectivity Status Pill */
.yt-network-status-pill {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(30px);
  background: rgba(20, 20, 24, 0.92);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: #fff;
  padding: 10px 22px;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  z-index: 9999;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s cubic-bezier(0.16, 1, 0.3, 1), transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.yt-network-status-pill.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateX(-50%) translateY(0);
}

.yt-network-status-pill .net-status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
}

.yt-network-status-pill.offline .net-status-dot {
  background: #f59e0b;
  box-shadow: 0 0 10px #f59e0b;
  animation: netPulse 1.5s infinite ease-in-out;
}

.yt-network-status-pill.online .net-status-dot {
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
}

@keyframes netPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.35); opacity: 0.55; }
}
"""

css_content += '\n' + css_to_add
with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)
print("SUCCESS: styles.css updated with card more button, quick thumb actions & network pill")
