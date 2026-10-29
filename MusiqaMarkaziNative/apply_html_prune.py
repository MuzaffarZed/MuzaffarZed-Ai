import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Prune nav-tabs in sidebar
old_nav = """        <div class="nav-section-label">Asosiy Bo'limlar</div>
        <div class="nav-tab active" data-tab="artists" onclick="switchTab('artists')">
          <span>🎤 San'atkorlar</span>
          <span class="nav-badge" id="navArtistsBadge">50+</span>
        </div>
        <div class="nav-tab" data-tab="collections" onclick="switchTab('collections')">
          <span>🎼 Janrlar & Uslublar</span>
          <span class="nav-badge">16+</span>
        </div>
        <div class="nav-tab" data-tab="search" onclick="switchTab('search')">
          <span>🔍 Qidiruv & Tanlash</span>
        </div>

        <div class="nav-section-label" style="margin-top:8px;">Media & Pleyer</div>
        <div class="nav-tab" data-tab="aimp" onclick="switchTab('aimp')">
          <span>🎧 Kutubxona & Pleylist</span>
          <span class="nav-badge" id="navLibraryBadge">0</span>
        </div>
        <div class="nav-tab" data-tab="simulator" onclick="switchTab('simulator')">
          <span>🎬 HD Kinozal (MP4)</span>
          <span class="nav-badge" id="navVideosBadge">0</span>
        </div>
        <div class="nav-tab" data-tab="queue" onclick="switchTab('queue')">
          <span>⚡ Yuklamalar (32-Oqim)</span>
          <span class="nav-badge" id="queueTabBadge"></span>
        </div>

        <div class="nav-section-label" style="margin-top:8px;">Kreativ & Studiya Pro</div>
        <div class="nav-tab" data-tab="kiosk" onclick="switchTab('kiosk')">
          <span>🏪 Fleshka Kiosk Pro</span>
          <span class="nav-badge" style="background:rgba(16,185,129,0.25);color:var(--emerald);">Avto</span>
        </div>
        <div class="nav-tab" data-tab="reels" onclick="switchTab('reels')">
          <span>🎬 9:16 Reels Fabrikasi</span>
          <span class="nav-badge" style="background:rgba(139,92,246,0.25);color:var(--purple);">HD</span>
        </div>
        <div class="nav-tab" data-tab="dj" onclick="switchTab('dj')">
          <span>🎚️ DJ Mashup Studiya</span>
          <span class="nav-badge" style="background:rgba(245,158,11,0.25);color:var(--gold);">Live</span>
        </div>

        <div class="nav-section-label" style="margin-top:8px;">Tizim & Vositalar</div>
        <div class="nav-tab" data-tab="turbo" onclick="switchTab('turbo')">
          <span>🚀 Turbo Doctor & RAM</span>
          <span class="nav-badge" id="navTurboBadge" style="background:rgba(56,189,248,0.25);color:var(--accent);">OK</span>
        </div>
        <div class="nav-tab" data-tab="vault" onclick="switchTab('vault')">
          <span>🔐 Kiber-Sandiq (AES)</span>
          <span class="nav-badge" id="navVaultBadge">0</span>
        </div>"""

new_nav = """        <div class="nav-section-label">Asosiy Katalog</div>
        <div class="nav-tab active" data-tab="artists" onclick="switchTab('artists')">
          <span>🎤 San'atkorlar</span>
          <span class="nav-badge" id="navArtistsBadge">50+</span>
        </div>
        <div class="nav-tab" data-tab="collections" onclick="switchTab('collections')">
          <span>🎼 Janrlar & To'plamlar</span>
          <span class="nav-badge">16+</span>
        </div>
        <div class="nav-tab" data-tab="search" onclick="switchTab('search')">
          <span>🔍 Qidiruv & Link</span>
        </div>

        <div class="nav-section-label" style="margin-top:8px;">Fleshka & Pleyer</div>
        <div class="nav-tab" data-tab="queue" onclick="switchTab('queue')">
          <span>⚡ Yuklamalar (32-Oqim)</span>
          <span class="nav-badge" id="queueTabBadge"></span>
        </div>
        <div class="nav-tab" data-tab="aimp" onclick="switchTab('aimp')">
          <span>🎧 Fleshka & Musiqa</span>
          <span class="nav-badge" id="navLibraryBadge">0</span>
        </div>
        <div class="nav-tab" data-tab="simulator" onclick="switchTab('simulator')">
          <span>🎬 HD Videoklip</span>
          <span class="nav-badge" id="navVideosBadge">0</span>
        </div>"""

assert old_nav in text, "old_nav not found!"
text = text.replace(old_nav, new_nav, 1)

# 2. Remove topbarRamPill
old_ram_pill = '<span id="topbarRamPill" class="telemetry-pill" onclick="switchTab(\'turbo\')" title="Tezkor RAM holati — Turbo Doctor\'ga o\'tish">⚡ RAM: --</span>'
if old_ram_pill in text:
    text = text.replace(old_ram_pill, "")

# 3. Remove bloat sections: tab-kiosk, tab-reels, tab-dj, tab-turbo, tab-vault
# Find start of tab-kiosk and end of tab-vault
kiosk_idx = text.find('<!-- TAB: FLESHKA KIOSK PRO (1-Click Auto USB Fill Engine) -->')
if kiosk_idx == -1:
    kiosk_idx = text.find('<section id="tab-kiosk"')

vault_end_str = '</section>\n\n      </main>'
vault_end_idx = text.find(vault_end_str, kiosk_idx)
assert kiosk_idx != -1 and vault_end_idx != -1, f"Indices not found: {kiosk_idx}, {vault_end_idx}"

text = text[:kiosk_idx] + '</main>' + text[vault_end_idx + len(vault_end_str) - len('</main>'):]

# 4. Remove duplicate/stem buttons in tab-aimp
old_dup_stem_aimp = """              <button class="btn btn-gold btn-sm" onclick="openDuplicatesModal()" title="Bir xil qo'shiqlarni akustik topish va ortiqchasini o'chirib joy bo'shatish">🧹 Dublikatlarni Tozalash</button>
              <button class="btn btn-purple btn-sm" onclick="openStemSeparatorModal()" title="Qo'shiqdan vokal va minusovkani sun'iy intellekt orqali ajratish">🎙️ AI Minusovka</button>"""
if old_dup_stem_aimp in text:
    text = text.replace(old_dup_stem_aimp, "")

# 5. Remove stem button in studio drawer
old_stem_drawer = '<button class="btn btn-purple btn-sm" onclick="openStemSeparatorModal()" title="AI bilan vokal va minusovkani alohida ajratish">🎙️ AI Stems</button>'
if old_stem_drawer in text:
    text = text.replace(old_stem_drawer, "")

# 6. Remove modals: vaultDecryptModal, qrModal, duplicatesModal, stemSeparatorModal
def remove_modal(t, modal_id):
    start = t.find(f'id="{modal_id}"')
    if start == -1:
        print(f"Modal {modal_id} not found")
        return t
    # find the opening <div before id
    div_start = t.rfind('<div', 0, start)
    # count balance of divs
    cur = div_start
    depth = 0
    while cur < len(t):
        if t[cur:cur+4] == '<div':
            depth += 1
            cur += 4
        elif t[cur:cur+6] == '</div>':
            depth -= 1
            cur += 6
            if depth == 0:
                break
        else:
            cur += 1
    # also remove any trailing whitespace or comments
    print(f"Removing modal {modal_id}: {div_start} to {cur}")
    return t[:div_start] + t[cur:]

for m_id in ['vaultDecryptModal', 'qrModal', 'duplicatesModal', 'stemSeparatorModal']:
    text = remove_modal(text, m_id)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("index.html updated successfully!")
