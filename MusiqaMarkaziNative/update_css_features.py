import sys, os
sys.stdout.reconfigure(encoding='utf-8')

css_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_card = """.media-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 11px;
  padding: 9px 11px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 7px;
  min-width: 0;
  min-height: 118px;
  transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
}"""

new_card = """.media-card {
  position: relative;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 11px;
  padding: 9px 11px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 7px;
  min-width: 0;
  min-height: 118px;
  transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
}
.media-card.favorited {
  border-color: rgba(245, 158, 11, 0.45);
  background: linear-gradient(180deg, rgba(245, 158, 11, 0.05) 0%, var(--bg-card) 100%);
  box-shadow: 0 4px 16px rgba(245, 158, 11, 0.08);
}
.card-fav-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.35);
  backdrop-filter: blur(4px);
  border: 1px solid var(--border);
  border-radius: 99px;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  cursor: pointer;
  transition: transform 0.15s ease, background 0.15s ease, border-color 0.15s ease;
  z-index: 2;
  line-height: 1;
  padding: 0;
}
.card-fav-btn:hover {
  transform: scale(1.18);
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}"""

assert old_card in text, "old_card not found in styles.css"
text = text.replace(old_card, new_card, 1)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("styles.css updated with favorite buttons and card styles!")
