css_v6 = """
/* ----------------------------------------------------
   SUBTITLES MENU, HISTORY TOOLBAR & SOUND MODAL
----------------------------------------------------- */

/* Subtitles Language Menu */
.yt-subtitles-menu {
  position: absolute;
  bottom: 52px;
  right: 180px;
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 12px;
  padding: 6px;
  min-width: 170px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  z-index: 100;
  animation: fadeIn 0.2s ease;
}

/* History Toolbar & Search */
.yt-history-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.yt-history-search-input {
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  color: #fff;
  width: 220px;
  outline: none;
  transition: border-color 0.2s ease;
}

.yt-history-search-input:focus {
  border-color: var(--yt-blue);
}

.yt-history-card-remove {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  z-index: 10;
}

.yt-card:hover .yt-history-card-remove {
  opacity: 1;
}

.yt-history-card-remove:hover {
  background: var(--yt-red);
  transform: scale(1.1);
}

/* Channel Search Box */
.yt-channel-search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 20px;
  padding: 4px 12px;
  width: 260px;
}

.yt-channel-search-box input {
  background: transparent;
  border: none;
  color: var(--yt-text-primary);
  font-size: 13px;
  outline: none;
  width: 100%;
}
"""

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

if '.yt-subtitles-menu' not in text:
    with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'a', encoding='utf-8') as f:
        f.write(css_v6)
    print("Appended v6 styles to styles.css!")
else:
    print("v6 styles already exist!")
