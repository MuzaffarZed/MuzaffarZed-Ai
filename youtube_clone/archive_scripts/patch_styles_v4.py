css_to_add = """
/* ----------------------------------------------------
   2X SPEED HOLD, NOTIFICATIONS, PROFILE & SHORTS PROGRESS
----------------------------------------------------- */

/* 2x Speed Hold Pill (YouTube 2026 signature feature) */
.yt-speed-2x-pill {
  position: absolute;
  top: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(-10px);
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  z-index: 25;
  pointer-events: none;
  opacity: 0;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}

.yt-speed-2x-pill.show {
  transform: translateX(-50%) translateY(0);
  opacity: 1;
}

.yt-speed-2x-pill .pill-indicator {
  display: inline-flex;
  gap: 2px;
  color: var(--yt-red);
  font-weight: 900;
}

/* Notifications Center Dropdown */
.yt-notifications-dropdown {
  position: absolute;
  top: 54px;
  right: 60px;
  width: 380px;
  max-height: 480px;
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 14px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: fadeIn 0.2s ease;
}

.yt-notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--yt-border);
  font-size: 16px;
  font-weight: 700;
}

.yt-notif-list {
  overflow-y: auto;
  max-height: 400px;
}

.yt-notif-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
}

.yt-notif-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.yt-notif-item.unread::before {
  content: '';
  position: absolute;
  left: 6px;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 6px;
  background: var(--yt-blue);
  border-radius: 50%;
}

.yt-notif-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.yt-notif-body {
  flex: 1;
  font-size: 13px;
  line-height: 1.4;
}

.yt-notif-time {
  font-size: 11px;
  color: var(--yt-text-secondary);
  margin-top: 4px;
}

.yt-notif-thumb {
  width: 64px;
  height: 38px;
  border-radius: 6px;
  object-fit: cover;
  flex-shrink: 0;
}

/* User Profile / Account Menu Card */
.yt-user-dropdown {
  position: absolute;
  top: 54px;
  right: 16px;
  width: 300px;
  background: var(--yt-surface);
  border: 1px solid var(--yt-border);
  border-radius: 14px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: fadeIn 0.2s ease;
  padding: 6px 0;
}

.yt-user-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--yt-border);
}

.yt-user-header img {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--yt-blue);
  object-fit: cover;
}

.yt-user-name {
  font-weight: 700;
  font-size: 15px;
  color: var(--yt-text-primary);
}

.yt-user-handle {
  font-size: 12px;
  color: var(--yt-text-secondary);
}

.yt-user-badge {
  display: inline-block;
  background: linear-gradient(135deg, #7928ca, #ff0080);
  color: white;
  font-size: 10px;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 10px;
  margin-top: 4px;
}

.yt-user-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.15s ease;
  color: var(--yt-text-primary);
}

.yt-user-menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--yt-blue);
}

.yt-user-menu-divider {
  height: 1px;
  background: var(--yt-border);
  margin: 6px 0;
}

/* Shorts Progress Bar */
.yt-short-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: rgba(255, 255, 255, 0.2);
  z-index: 35;
}

.yt-short-progress-fill {
  height: 100%;
  width: 0%;
  background: var(--yt-red);
  transition: width 0.1s linear;
}
"""

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

if '.yt-speed-2x-pill' not in text:
    with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\styles.css', 'a', encoding='utf-8') as f:
        f.write(css_to_add)
    print("Appended v4 styles to styles.css!")
else:
    print("v4 styles already present!")
