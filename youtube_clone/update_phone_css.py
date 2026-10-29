# -*- coding: utf-8 -*-

css_path = r"C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css"
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

phone_css = """
/* Phone Connect Button & QR Modal Styling */
.yt-phone-connect-btn {
  background: rgba(16, 185, 129, 0.12) !important;
  color: #10b981 !important;
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  border-radius: 20px !important;
  width: auto !important;
  padding: 0 12px !important;
  gap: 6px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  display: inline-flex !important;
  align-items: center !important;
  cursor: pointer !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.yt-phone-connect-btn:hover {
  background: rgba(16, 185, 129, 0.22) !important;
  border-color: #10b981 !important;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.35) !important;
  transform: translateY(-1px);
}

@media (max-width: 900px) {
  .yt-phone-connect-btn span {
    display: none !important;
  }
  .yt-phone-connect-btn {
    width: 36px !important;
    padding: 0 !important;
    justify-content: center !important;
  }
}
"""

if '.yt-phone-connect-btn' not in css_content:
    css_content += phone_css
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Added phone CSS styles to styles.css")
else:
    print("Phone CSS styles already present")
