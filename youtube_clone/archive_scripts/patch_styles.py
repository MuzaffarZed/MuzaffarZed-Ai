css_to_append = """
/* ----------------------------------------------------
   YOUTUBE PRO CUSTOM CONTEXT MENU & TIMESTAMPS
----------------------------------------------------- */
.yt-context-menu {
  position: fixed;
  background: rgba(24, 24, 27, 0.96);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.8);
  padding: 6px;
  min-width: 260px;
  z-index: 9999;
  user-select: none;
}

.yt-context-menu .yt-dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 14px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--yt-text-primary);
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
}

.yt-context-menu .yt-dropdown-item:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateX(2px);
}

.yt-context-menu .yt-dropdown-item i {
  color: var(--yt-text-secondary);
}

.yt-context-menu .yt-dropdown-item:hover i {
  color: var(--yt-blue);
}

.yt-context-divider {
  height: 1px;
  background: var(--yt-border);
  margin: 5px 6px;
}

/* Clickable Timestamps in Descriptions & Comments */
.yt-timestamp-link {
  color: var(--yt-blue);
  background: rgba(62, 166, 255, 0.14);
  padding: 2px 7px;
  border-radius: 4px;
  font-weight: 600;
  font-family: monospace;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-block;
  margin: 0 2px;
}

.yt-timestamp-link:hover {
  background: var(--yt-blue);
  color: #000;
  text-decoration: none;
  transform: scale(1.05);
}
"""

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    current = f.read()

if '.yt-context-menu' not in current:
    with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'a', encoding='utf-8') as f:
        f.write(css_to_append)
    print("Successfully appended context menu & timestamp styles to styles.css!")
else:
    print("Styles already present.")
