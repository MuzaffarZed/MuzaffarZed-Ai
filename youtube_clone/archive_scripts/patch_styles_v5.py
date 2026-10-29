css_v5 = """
/* ----------------------------------------------------
   SUBSCRIPTIONS FEED, SLEEP PRESETS & RECENT SEARCHES
----------------------------------------------------- */

/* Subscriptions Feed */
.yt-subs-channels-row {
  display: flex;
  gap: 18px;
  overflow-x: auto;
  padding: 10px 0 16px;
  border-bottom: 1px solid var(--yt-border);
  scrollbar-width: thin;
}

.yt-subs-channel-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  min-width: 72px;
  transition: transform 0.15s ease;
  position: relative;
}

.yt-subs-channel-item:hover {
  transform: translateY(-2px);
}

.yt-subs-avatar-wrap {
  position: relative;
  width: 56px;
  height: 56px;
}

.yt-subs-avatar-wrap img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
}

.yt-subs-channel-item.active .yt-subs-avatar-wrap img {
  border-color: var(--yt-blue);
}

.yt-subs-unread-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  background: var(--yt-blue);
  border-radius: 50%;
  border: 2px solid var(--yt-bg);
}

.yt-subs-channel-name {
  font-size: 11px;
  font-weight: 600;
  color: var(--yt-text-secondary);
  text-align: center;
  max-width: 72px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.yt-subs-channel-item.active .yt-subs-channel-name {
  color: var(--yt-text-primary);
  font-weight: 700;
}

/* Sleep Timer Presets Dropdown */
.yt-sleep-dropdown {
  position: absolute;
  top: 54px;
  right: 240px;
  width: 220px;
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  z-index: 1000;
  padding: 6px;
  animation: fadeIn 0.2s ease;
}

/* Recent Search Suggestion Item */
.yt-recent-search-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s ease;
}

.yt-recent-search-row:hover {
  background: rgba(255, 255, 255, 0.08);
}

.yt-recent-search-left {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: var(--yt-text-primary);
}

.yt-btn-remove-recent {
  background: transparent;
  border: none;
  color: var(--yt-text-secondary);
  cursor: pointer;
  padding: 2px 6px;
  font-size: 11px;
  border-radius: 4px;
}

.yt-btn-remove-recent:hover {
  color: var(--yt-red);
}
"""

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

if '.yt-subs-channels-row' not in text:
    with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'a', encoding='utf-8') as f:
        f.write(css_v5)
    print("Appended v5 styles successfully!")
else:
    print("v5 styles already exist!")
