# 1. Update index.html
index_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read().replace('\r\n', '\n')

old_ctx = """    <div class="yt-dropdown-item" id="ctx-pip">
      <i data-lucide="picture-in-picture-2" style="width: 16px; height: 16px;"></i>
      <span>Picture-in-Picture</span>
    </div>"""

new_ctx = """    <div class="yt-dropdown-item" id="ctx-pip">
      <i data-lucide="picture-in-picture-2" style="width: 16px; height: 16px;"></i>
      <span>Picture-in-Picture</span>
    </div>
    <div class="yt-dropdown-item" id="ctx-zoom-fit">
      <i data-lucide="maximize-2" style="width: 16px; height: 16px;"></i>
      <span id="ctx-zoom-text">Kattalashtirish (Zoom to fill)</span>
    </div>"""

if old_ctx in html:
    html = html.replace(old_ctx, new_ctx, 1)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: index.html updated with ctx-zoom-fit")
else:
    print("WARNING: old_ctx not found in index.html")

# 2. Update styles.css
css_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read().replace('\r\n', '\n')

css_zoom = """
/* Zoom to Fill Cinema Mode */
.yt-video-element.zoom-fill {
  object-fit: cover !important;
}
"""

if '.yt-video-element.zoom-fill' not in css:
    css += '\n' + css_zoom
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("SUCCESS: styles.css updated with .zoom-fill")
else:
    print("styles.css already has .zoom-fill")

# 3. Update app.js
app_path = r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    c = f.read().replace('\r\n', '\n')

# Add toggleZoomFill method
zoom_method = """    toggleZoomFill() {
      if (!this.videoElement) return;
      const isZoomed = this.videoElement.classList.toggle('zoom-fill');
      const zoomText = document.getElementById('ctx-zoom-text');
      if (zoomText) zoomText.textContent = isZoomed ? "Asl o'lcham (Fit screen)" : "Kattalashtirish (Zoom to fill)";
      this.showToast(isZoomed ? "Zoom: To'liq qoplash (Cover)" : "Zoom: Asl o'lcham (Contain)");
    }
"""

target_before_wheel = "    // MOUSE WHEEL VOLUME CONTROL"
if target_before_wheel in c:
    c = c.replace(target_before_wheel, zoom_method + "\n    " + target_before_wheel, 1)
    print("SUCCESS: toggleZoomFill method added")
else:
    print("WARNING: target_before_wheel not found")

# Bind in initVideoContextMenu()
old_pip_bind = """      if (this.ctxPip) {
        this.ctxPip.addEventListener('click', () => {
          this.btnPipNative.click();
          this.playerContextMenu.style.display = 'none';
        });
      }"""

new_pip_bind = """      if (this.ctxPip) {
        this.ctxPip.addEventListener('click', () => {
          this.btnPipNative.click();
          this.playerContextMenu.style.display = 'none';
        });
      }

      const ctxZoom = document.getElementById('ctx-zoom-fit');
      if (ctxZoom) {
        ctxZoom.addEventListener('click', () => {
          this.toggleZoomFill();
          this.playerContextMenu.style.display = 'none';
        });
      }"""

if old_pip_bind in c:
    c = c.replace(old_pip_bind, new_pip_bind, 1)
    print("SUCCESS: ctx-zoom-fit click listener added")
else:
    print("WARNING: old_pip_bind not found")

# Bind 'z' key in keydown
old_z_key = "} else if (e.key === 'p') {"
new_z_key = """} else if (e.key === 'z' || e.key === 'Z') {
            e.preventDefault();
            this.toggleZoomFill();
          } else if (e.key === 'p') {"""

if old_z_key in c:
    c = c.replace(old_z_key, new_z_key, 1)
    print("SUCCESS: 'z' key shortcut added")
else:
    print("WARNING: old_z_key not found")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(c)
