import sys, os
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update omnibox to add clipboard paste button
old_omnibox = """        <div class="omnibox-search">
          <span style="font-size:13px;color:var(--accent);">🔍</span>
          <input type="text" id="globalSearchInput" placeholder="Qo'shiq, san'atkor yoki YouTube link izlash (Ctrl+F)..." />
          <button class="btn btn-ghost btn-sm btn-pill" style="padding:3px 7px;" onclick="startVoiceSearch()" title="Ovoz bilan qidirish">🎙️</button>
          <button class="btn btn-sm btn-pill" style="padding:4px 12px;" onclick="triggerGlobalSearch()">Topish</button>
        </div>"""

new_omnibox = """        <div class="omnibox-search">
          <span style="font-size:13px;color:var(--accent);">🔍</span>
          <input type="text" id="globalSearchInput" placeholder="Qo'shiq, san'atkor yoki YouTube link izlash (Ctrl+F)..." />
          <button class="btn btn-ghost btn-sm btn-pill" style="padding:3px 7px;" onclick="pasteClipboardToSearch()" title="Xotiradan (Ctrl+V) link yoki matnni qo'yish">📋</button>
          <button class="btn btn-ghost btn-sm btn-pill" style="padding:3px 7px;" onclick="startVoiceSearch()" title="Ovoz bilan qidirish">🎙️</button>
          <button class="btn btn-sm btn-pill" style="padding:4px 12px;" onclick="triggerGlobalSearch()">Topish</button>
        </div>"""

assert old_omnibox in text, "old_omnibox not found"
text = text.replace(old_omnibox, new_omnibox, 1)

# 2. Add Language Selector in topbar right before skinSelector
old_skin = """          <select id="skinSelector" class="select-ctrl" onchange="changeSkin(this.value)" title="Dastur rang temasi">"""
new_skin = """          <select id="langSelector" class="select-ctrl" onchange="changeLanguage(this.value)" title="Dastur tili / Язык / Language">
            <option value="uz" selected>🇺🇿 O'zbek</option>
            <option value="ru">🇷🇺 Русский</option>
            <option value="en">🇬🇧 English</option>
          </select>

          <select id="skinSelector" class="select-ctrl" onchange="changeSkin(this.value)" title="Dastur rang temasi">"""

assert old_skin in text, "old_skin not found"
text = text.replace(old_skin, new_skin, 1)

# 3. Add Fleshka Cockpit to tab-collections
old_col_header = """        <!-- TAB 2: 16+ JANRLAR & USLUBLAR -->
        <section id="tab-collections" class="tab-pane">
          <div class="pane-toolbar">"""

new_col_header = """        <!-- TAB 2: 16+ JANRLAR & USLUBLAR -->
        <section id="tab-collections" class="tab-pane">
          <!-- Direct-to-USB Fleshka Cockpit Bar -->
          <div class="fleshka-cockpit-bar" style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.22);border-radius:10px;padding:8px 12px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:20px;">🎼</span>
              <div>
                <div style="font-size:12px;font-weight:900;color:var(--emerald);">Janrlar & Avto-To'plamlar: Fleshkaga 1-Klikda Yozish</div>
                <div style="font-size:10px;color:var(--text-sub);">Har bir to'plam to'g'ridan-to'g'ri fleshkadagi o'z nomidagi toza papkaga (001-raqamlangan, FAT32 tartibli) tushadi</div>
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
              <span style="font-size:11px;font-weight:700;color:var(--gold);">🎯 Fleshka / Manzil:</span>
              <select id="collectionsUsbSelect" class="select-ctrl" style="min-width:210px;font-weight:700;color:var(--emerald);" onchange="onArtistUsbSelectChange(this.value)" title="Qo'shiqlar to'g'ridan-to'g'ri qayerga saqlansin?"></select>
              <button class="btn btn-ghost btn-sm" onclick="refreshUsbDrives()" title="Fleshkani qayta tekshirish">🔄</button>
              <button class="btn btn-emerald btn-sm" onclick="openActiveUsbFolder()" title="Fleshkadagi musiqalar papkasini ochish">📂 Fleshkani Ochish</button>
              <button class="btn btn-ghost btn-sm" onclick="formatActiveUsbPrompt()" style="color:#ef4444;" title="Fleshkani magnitola o'qiydigan FAT32 formatga o'tkazish">🩺 FAT32 Format</button>
            </div>
          </div>

          <div class="pane-toolbar">"""

assert old_col_header in text, "old_col_header not found"
text = text.replace(old_col_header, new_col_header, 1)

# 4. In tab-search, add paste button and smart suggestion banner
old_search_tb = """              <input type="text" id="searchQueryInput" class="input-field" style="flex:1;" placeholder="🔍 Qo'shiq nomi, san'atkor, klip yoki YouTube linkni kiriting..." onkeydown="if(event.key==='Enter') runInteractiveSearch()" />"""
new_search_tb = """              <input type="text" id="searchQueryInput" class="input-field" style="flex:1;" placeholder="🔍 Qo'shiq nomi, san'atkor, klip yoki YouTube linkni kiriting..." onkeydown="if(event.key==='Enter') runInteractiveSearch()" />
              <button class="btn btn-ghost btn-sm" onclick="pasteClipboardToSearchInput()" title="Xotiradan (Ctrl+V) link yoki matnni qo'yish" style="padding:4px 8px;">📋 Qo'yish</button>"""

assert old_search_tb in text, "old_search_tb not found"
text = text.replace(old_search_tb, new_search_tb, 1)

# Add smart suggestion banner right after pane-toolbar in tab-search
old_search_card = """          <!-- DIRECT YOUTUBE LINK 1-CLICK ACTION CARD -->"""
new_search_card = """          <!-- SMART ARTIST CATALOG COLLABORATION BANNER -->
          <div id="searchArtistSuggestionBanner" style="display:none;margin-bottom:8px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.28);border-radius:10px;padding:8px 12px;align-items:center;justify-content:space-between;gap:8px;">
            <div style="display:flex;align-items:center;gap:8px;min-width:0;">
              <span style="font-size:18px;">💡</span>
              <div style="min-width:0;">
                <span id="searchArtistSuggestionText" style="font-size:11.5px;font-weight:800;color:var(--gold);"></span>
                <div style="font-size:10px;color:var(--text-sub);">Katalogdagi barcha xitlarini qidirib o'tirmasdan, to'g'ridan-to'g'ri fleshkadagi o'z papkasiga 1-bosishda yozishingiz mumkin!</div>
              </div>
            </div>
            <button class="btn btn-emerald btn-sm" id="btnSearchArtistDirectDownload" style="font-weight:800;padding:5px 14px;white-space:nowrap;">⚡ Fleshkaga 1-Klikda Yozish</button>
          </div>

          <!-- DIRECT YOUTUBE LINK 1-CLICK ACTION CARD -->"""

assert old_search_card in text, "old_search_card not found"
text = text.replace(old_search_card, new_search_card, 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("ui/index.html successfully updated with high-synergy controls!")
