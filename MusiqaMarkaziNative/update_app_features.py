import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

app_path = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add favoriteArtists and currentLang to state
old_state_part = """  minDurationSec: parseInt(localStorage.getItem("musiqa_min_duration"), 10) || 96,"""
new_state_part = """  minDurationSec: parseInt(localStorage.getItem("musiqa_min_duration"), 10) || 96,
  favoriteArtists: JSON.parse(localStorage.getItem("musiqa_fav_artists") || "[]"),
  currentLang: localStorage.getItem("musiqa_lang") || "uz","""

assert old_state_part in text, "old_state_part not found in app.js"
text = text.replace(old_state_part, new_state_part, 1)

# 2. Update renderArtistsGrid and renderCollectionsGrid
old_artists_grid = """function renderArtistsGrid() {
  const q = (document.getElementById("artistFilterInput").value || "").trim().toLowerCase();
  const filtered = state.artists.filter(a => {
    if (state.selectedArtistCategory !== "Barchasi" && a.category !== state.selectedArtistCategory) return false;
    if (q && !a.name.toLowerCase().includes(q) && !(a.desc || "").toLowerCase().includes(q)) return false;
    return true;
  });

  document.getElementById("artistCountBadge").textContent = `${filtered.length} ta san'atkor`;
  const navBadge = document.getElementById("navArtistsBadge");
  if (navBadge) navBadge.textContent = `${state.artists.length}`;

  const grid = document.getElementById("artistsGrid");
  if (filtered.length === 0) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--text-sub);">
      San'atkor topilmadi. <b>"➕ San'atkor Qo'shish"</b> tugmasini bosing yoki Qidiruv bo'limidan izlang!
    </div>`;
    return;
  }

  grid.innerHTML = filtered.map((art, i) => {
    const monogram = getArtistMonogram(art.name);
    const grad = AVATAR_GRADIENTS[i % AVATAR_GRADIENTS.length];
    return `
      <div class="media-card">
        <div class="card-top">
          <div class="artist-avatar" style="background:${grad};">${escapeHtml(monogram)}</div>
          <div class="card-info">
            <div class="card-title">${escapeHtml(art.name)}</div>
            <div class="card-sub">${escapeHtml(art.desc || "Eng sara xit qo'shiqlar")}</div>
            <span class="card-badge">${escapeHtml(art.category)}</span>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-emerald btn-sm btn-card-turbo" onclick="downloadArtistTurbo(${i})" title="Belgilangan sonda barcha xitlarini yuklash">⚡ Barchasini Yuklash</button>
          <div class="card-sub-actions">
            <button class="btn btn-ghost btn-sm" onclick="previewArtistTracks(${i})" title="Qo'shiqlar ro'yxatini ko'rib tanlab yuklash">🔍 Tanlash</button>
            <button class="btn btn-gold btn-sm" onclick="downloadArtistTop5(${i})" title="Eng mashhur 5 ta xitini 1 bosishda yuklash">🔥 Top-5</button>
          </div>
        </div>
      </div>
    `;
  }).join("");
  grid._filteredList = filtered;
}

function renderCollectionsGrid() {
  const grid = document.getElementById("collectionsGrid");
  grid.innerHTML = state.collections.map((col, i) => {
    const grad = AVATAR_GRADIENTS[(i + 2) % AVATAR_GRADIENTS.length];
    return `
      <div class="media-card">
        <div class="card-top">
          <div class="artist-avatar" style="background:${grad};font-size:18px;">🎼</div>
          <div class="card-info">
            <div class="card-title">${escapeHtml(col.title)}</div>
            <div class="card-sub">📁 ${escapeHtml(col.targetFolder)} • ${escapeHtml(col.desc)}</div>
            <span class="card-badge">${escapeHtml(col.badge || "2026")}</span>
          </div>
        </div>
        <div class="card-actions two-cols">
          <button class="btn btn-ghost btn-sm" onclick="previewCollectionTracks(${i})">🔍 Tanlash</button>
          <button class="btn btn-emerald btn-sm" onclick="downloadCollectionTurbo(${i})">⚡ Yuklash</button>
        </div>
      </div>
    `;
  }).join("");
}"""

new_artists_grid = """function toggleFavoriteArtist(name, event) {
  if (event) event.stopPropagation();
  if (!state.favoriteArtists) state.favoriteArtists = [];
  const idx = state.favoriteArtists.indexOf(name);
  if (idx >= 0) {
    state.favoriteArtists.splice(idx, 1);
    showToast(`🤍 "${name}" sevimlilardan olib tashlandi`, "info");
  } else {
    state.favoriteArtists.push(name);
    showToast(`❤️ "${name}" sevimlilarga qo'shildi!`, "success");
  }
  localStorage.setItem("musiqa_fav_artists", JSON.stringify(state.favoriteArtists));
  renderArtistsGrid();
}

function searchAndDownloadFromCatalog(name) {
  document.getElementById("searchQueryInput").value = name;
  document.getElementById("targetFolderInput").value = name;
  switchTab("search");
  runInteractiveSearch();
}

function renderArtistsGrid() {
  const q = (document.getElementById("artistFilterInput")?.value || "").trim().toLowerCase();
  const favs = state.favoriteArtists || [];
  
  const filtered = state.artists.filter(a => {
    if (state.selectedArtistCategory === "❤️ Sevimlilar") {
      if (!favs.includes(a.name)) return false;
    } else if (state.selectedArtistCategory !== "Barchasi" && a.category !== state.selectedArtistCategory) {
      return false;
    }
    if (q && !a.name.toLowerCase().includes(q) && !(a.desc || "").toLowerCase().includes(q)) return false;
    return true;
  });

  // Sort so favorited artists always appear first
  filtered.sort((a, b) => {
    const aFav = favs.includes(a.name);
    const bFav = favs.includes(b.name);
    if (aFav && !bFav) return -1;
    if (!aFav && bFav) return 1;
    return 0;
  });

  const countEl = document.getElementById("artistCountBadge");
  if (countEl) countEl.textContent = `${filtered.length} ta san'atkor`;
  const navBadge = document.getElementById("navArtistsBadge");
  if (navBadge) navBadge.textContent = `${state.artists.length}`;

  const grid = document.getElementById("artistsGrid");
  if (!grid) return;

  if (filtered.length === 0) {
    if (state.selectedArtistCategory === "❤️ Sevimlilar") {
      grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:44px 20px;background:var(--bg-card);border-radius:12px;border:1px solid var(--border);color:var(--text-sub);">
        <div style="font-size:32px;margin-bottom:8px;">🤍</div>
        <div style="font-size:14px;font-weight:800;color:var(--text-main);margin-bottom:4px;">Hozircha sevimli san'atkorlar tanlanmagan</div>
        <div style="font-size:11.5px;">Istalgan san'atkor kartasidagi ❤️ yurakchani bosib, sevimli qilib qo'yishingiz mumkin!</div>
      </div>`;
      grid._filteredList = [];
      return;
    }
    grid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:36px 20px;background:var(--bg-card);border:1px dashed var(--accent);border-radius:14px;">
        <div style="font-size:26px;margin-bottom:8px;">🔍</div>
        <div style="font-size:14.5px;font-weight:800;color:var(--text-main);margin-bottom:4px;">
          "${escapeHtml(q)}" katalogda topilmadi
        </div>
        <div style="font-size:11.5px;color:var(--text-sub);max-width:480px;margin:0 auto 14px;">
          Hechqisi yo'q! Bitta tugma bilan ushbu san'atkorning eng yangi va sara xitlarini YouTube'dan topib, to'g'ridan-to'g'ri fleshkaga yozib olishingiz mumkin.
        </div>
        <button class="btn btn-emerald btn-sm" onclick="searchAndDownloadFromCatalog('${escapeHtml(q)}')" style="font-weight:800;padding:8px 20px;">
          ⚡ Qidiruvda Topish va Fleshkaga Yozish
        </button>
      </div>`;
    grid._filteredList = [];
    return;
  }

  grid.innerHTML = filtered.map((art, i) => {
    const monogram = getArtistMonogram(art.name);
    const grad = AVATAR_GRADIENTS[i % AVATAR_GRADIENTS.length];
    const isFav = favs.includes(art.name);
    return `
      <div class="media-card ${isFav ? "favorited" : ""}">
        <button class="card-fav-btn" onclick="toggleFavoriteArtist('${escapeHtml(art.name)}', event)" title="${isFav ? "Sevimlilardan olib tashlash" : "Sevimlilarga qo'shish (❤️)"}">
          ${isFav ? "❤️" : "🤍"}
        </button>
        <div class="card-top">
          <div class="artist-avatar" style="background:${grad};">${escapeHtml(monogram)}</div>
          <div class="card-info">
            <div class="card-title">${escapeHtml(art.name)}</div>
            <div class="card-sub">${escapeHtml(art.desc || "Eng sara xit qo'shiqlar")}</div>
            <span class="card-badge">${escapeHtml(art.category)}</span>
          </div>
        </div>
        <div class="card-actions">
          <button class="btn btn-emerald btn-sm btn-card-turbo" onclick="downloadArtistTurbo(${i})" title="To'g'ridan-to'g'ri fleshkadagi o'z papkasiga yuklash">⚡ Barchasini Yuklash</button>
          <div class="card-sub-actions">
            <button class="btn btn-ghost btn-sm" onclick="previewArtistTracks(${i})" title="Qo'shiqlar ro'yxatini ko'rib tanlab yuklash">🔍 Tanlash</button>
            <button class="btn btn-gold btn-sm" onclick="downloadArtistTop5(${i})" title="Eng mashhur 5 ta xitini 1 bosishda yuklash">🔥 Top-5</button>
          </div>
        </div>
      </div>
    `;
  }).join("");
  grid._filteredList = filtered;
}

function renderCollectionsGrid() {
  const grid = document.getElementById("collectionsGrid");
  if (!grid) return;
  grid.innerHTML = state.collections.map((col, i) => {
    const grad = AVATAR_GRADIENTS[(i + 2) % AVATAR_GRADIENTS.length];
    const count = col.count || 20;
    return `
      <div class="media-card">
        <div class="card-top">
          <div class="artist-avatar" style="background:${grad};font-size:18px;">🎼</div>
          <div class="card-info">
            <div class="card-title">${escapeHtml(col.title)}</div>
            <div class="card-sub">📁 ${escapeHtml(col.targetFolder)} • ${escapeHtml(col.desc)}</div>
            <span class="card-badge">${escapeHtml(col.badge || "2026")} • ${count} ta trek</span>
          </div>
        </div>
        <div class="card-actions two-cols">
          <button class="btn btn-ghost btn-sm" onclick="previewCollectionTracks(${i})" title="Qidiruvda ko'rish va tanlab yuklash">🔍 Tanlash</button>
          <button class="btn btn-emerald btn-sm" onclick="downloadCollectionTurbo(${i})" title="Fleshkadagi o'z papkasiga 1-bosishda yozish">⚡ Fleshkaga Yozish</button>
        </div>
      </div>
    `;
  }).join("");
}"""

assert old_artists_grid in text, "old_artists_grid not found in app.js"
text = text.replace(old_artists_grid, new_artists_grid, 1)

# 3. Add clipboard paste and search artist suggestion functions
clipboard_funcs = """
async function pasteClipboardToSearch() {
  try {
    const textVal = await navigator.clipboard.readText();
    if (textVal && textVal.trim()) {
      document.getElementById("globalSearchInput").value = textVal.trim();
      triggerGlobalSearch();
    } else {
      showToast("Xotirada (Clipboard) matn topilmadi", "info");
    }
  } catch (err) {
    document.getElementById("globalSearchInput").focus();
    showToast("Havolani qo'yish uchun Ctrl+V bosing", "info");
  }
}

async function pasteClipboardToSearchInput() {
  try {
    const textVal = await navigator.clipboard.readText();
    if (textVal && textVal.trim()) {
      const input = document.getElementById("searchQueryInput");
      input.value = textVal.trim();
      showToast("📋 Havola muvaffaqiyatli qo'yildi!", "success");
      runInteractiveSearch();
    } else {
      showToast("Xotirada (Clipboard) havola topilmadi", "info");
    }
  } catch (err) {
    const input = document.getElementById("searchQueryInput");
    input.focus();
    showToast("Havolani qo'yish uchun Ctrl+V bosing", "info");
  }
}

function checkSearchArtistSuggestion(query) {
  const q = (query || "").trim().toLowerCase();
  const banner = document.getElementById("searchArtistSuggestionBanner");
  const textEl = document.getElementById("searchArtistSuggestionText");
  const btn = document.getElementById("btnSearchArtistDirectDownload");
  if (!banner || !textEl || !btn) return;

  if (q.length < 2) {
    banner.style.display = "none";
    return;
  }

  const match = state.artists.find(a => a.name.toLowerCase().includes(q));
  if (match) {
    banner.style.display = "flex";
    textEl.textContent = `Katalogdagi San'atkor: ${match.name} (${match.category})`;
    btn.onclick = () => {
      const idx = state.artists.indexOf(match);
      downloadArtistTurbo(idx);
    };
  } else {
    banner.style.display = "none";
  }
}

// Multi-Language Localization Engine (O'zbekcha / Русский / English)
const I18N = {
  uz: {
    navArtists: "🎤 San'atkorlar",
    navCollections: "🎼 Janrlar & To'plamlar",
    navSearch: "🔍 Qidiruv & Link",
    navQueue: "⚡ Yuklamalar (32-Oqim)",
    navMusic: "🎧 Fleshka & Musiqa",
    navVideo: "🎬 HD Videoklip",
    openUsb: "📂 Fleshkani Ochish",
    formatFat32: "🩺 FAT32 Format"
  },
  ru: {
    navArtists: "🎤 Артисты",
    navCollections: "🎼 Жанры и Сборники",
    navSearch: "🔍 Поиск и Ссылки",
    navQueue: "⚡ Загрузки (32 потока)",
    navMusic: "🎧 Флешка и Музыка",
    navVideo: "🎬 HD Видеоклипы",
    openUsb: "📂 Открыть флешку",
    formatFat32: "🩺 Формат FAT32"
  },
  en: {
    navArtists: "🎤 Artists",
    navCollections: "🎼 Genres & Bundles",
    navSearch: "🔍 Search & Link",
    navQueue: "⚡ Downloads (32-Stream)",
    navMusic: "🎧 Flash Drive & Music",
    navVideo: "🎬 HD Video Clips",
    openUsb: "📂 Open Flash Drive",
    formatFat32: "🩺 Format FAT32"
  }
};

function changeLanguage(lang) {
  state.currentLang = lang || "uz";
  localStorage.setItem("musiqa_lang", state.currentLang);
  const dict = I18N[state.currentLang] || I18N.uz;

  const tArtists = document.querySelector('.nav-tab[data-tab="artists"] span:first-child');
  if (tArtists) tArtists.textContent = dict.navArtists;

  const tCollections = document.querySelector('.nav-tab[data-tab="collections"] span:first-child');
  if (tCollections) tCollections.textContent = dict.navCollections;

  const tSearch = document.querySelector('.nav-tab[data-tab="search"] span:first-child');
  if (tSearch) tSearch.textContent = dict.navSearch;

  const tQueue = document.querySelector('.nav-tab[data-tab="queue"] span:first-child');
  if (tQueue) tQueue.textContent = dict.navQueue;

  const tMusic = document.querySelector('.nav-tab[data-tab="aimp"] span:first-child');
  if (tMusic) tMusic.textContent = dict.navMusic;

  const tVideo = document.querySelector('.nav-tab[data-tab="simulator"] span:first-child');
  if (tVideo) tVideo.textContent = dict.navVideo;

  const sel = document.getElementById("langSelector");
  if (sel && sel.value !== state.currentLang) sel.value = state.currentLang;

  showToast(`🌐 Til: ${state.currentLang.toUpperCase()} faollashtirildi`, "info");
}
"""

anchor = "function triggerGlobalSearch()"
text = text.replace(anchor, clipboard_funcs + "\n" + anchor, 1)

# 4. Synchronize both artistUsbSelect and collectionsUsbSelect
old_on_artist_usb = """function onArtistUsbSelectChange(val) {
  state.baseDir = val;
  refreshUsbDrives();
  refreshLibrary();
  showToast(`🎯 Manzil: ${val} belgilandi`, "info");
}"""

new_on_artist_usb = """function onArtistUsbSelectChange(val) {
  state.baseDir = val;
  const s1 = document.getElementById("artistUsbSelect");
  const s2 = document.getElementById("collectionsUsbSelect");
  if (s1 && s1.value !== val) s1.value = val;
  if (s2 && s2.value !== val) s2.value = val;
  refreshUsbDrives();
  refreshLibrary();
  showToast(`🎯 Fleshka Manzili: ${val} belgilandi`, "success");
}"""

if old_on_artist_usb in text:
    text = text.replace(old_on_artist_usb, new_on_artist_usb, 1)

# In renderUsbDrivesSelect, populate collectionsUsbSelect as well
old_populate_usb = """  const sel = document.getElementById("artistUsbSelect");
  if (!sel) return;
  sel.innerHTML = state.detectedDrives.map(d => {
    const isSelected = d.root.toLowerCase() === (state.baseDir || "").toLowerCase();
    const warn = d.fs !== "FAT32" ? " ⚠️ (Tavsiya: FAT32)" : " ✅ (FAT32)";
    return `<option value="${escapeHtml(d.root)}" ${isSelected ? "selected" : ""}>
      💾 ${escapeHtml(d.label)}: ${escapeHtml(d.root)} (${d.freeGb} GB bo'sh${warn})
    </option>`;
  }).join("");"""

new_populate_usb = """  const sel1 = document.getElementById("artistUsbSelect");
  const sel2 = document.getElementById("collectionsUsbSelect");
  const optionsHtml = state.detectedDrives.map(d => {
    const isSelected = d.root.toLowerCase() === (state.baseDir || "").toLowerCase();
    const warn = d.fs !== "FAT32" ? " ⚠️ (Tavsiya: FAT32)" : " ✅ (FAT32)";
    return `<option value="${escapeHtml(d.root)}" ${isSelected ? "selected" : ""}>
      💾 ${escapeHtml(d.label)}: ${escapeHtml(d.root)} (${d.freeGb} GB bo'sh${warn})
    </option>`;
  }).join("");

  if (sel1) sel1.innerHTML = optionsHtml;
  if (sel2) sel2.innerHTML = optionsHtml;"""

if old_populate_usb in text:
    text = text.replace(old_populate_usb, new_populate_usb, 1)

# Add event listener for searchQueryInput on initialization
old_init_search = 'document.getElementById("searchQueryInput").addEventListener("input",'
if old_init_search not in text:
    init_anchor = 'document.getElementById("searchQueryInput").addEventListener("keydown",'
    new_input_listener = """document.getElementById("searchQueryInput")?.addEventListener("input", e => {
  checkSearchArtistSuggestion(e.target.value);
});\n"""
    text = text.replace(init_anchor, new_input_listener + init_anchor, 1)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("ui/app.js updated with high-synergy features, favorites, and multi-language engine!")
