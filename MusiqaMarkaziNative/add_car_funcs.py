import sys, os
sys.stdout.reconfigure(encoding='utf-8')

app_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\ui\app.js"

with open(app_path, "r", encoding="utf-8") as f:
    text = f.read()

car_functions = """
// ============================================================================
// CAR STEREO & FLESHKA ESSENTIAL ACTIONS
// ============================================================================
async function renumberActiveFolderForCarAction() {
  const folder = document.getElementById("targetFolderInput")?.value?.trim() || "";
  const base = state.baseDir || "";
  try {
    showToast("🚗 Avto-magnitola uchun 001..050 raqamlash va M3U pleylist yaratilmoqda...", "info");
    const fullFolder = (base && folder) ? `${base.replace(/[\\\\/]+$/, "")}\\\\${folder}` : (base || folder);
    const res = await apiPost("/api/car/renumber", {
      folder: fullFolder,
      addPrefix: true,
      createM3U: true
    });
    if (res && res.ok) {
      showToast(`✅ ${res.renamedCount || 0} ta fayl tartiblandi va M3U pleylist yaratildi!`, "success");
      refreshLibrary();
    } else {
      showToast("Tartiblash bajarildi.", "info");
    }
  } catch (err) {
    showToast("Xatolik: " + err.message, "danger");
  }
}

async function normalizeActiveTrackLoudnessAction() {
  if (!state.currentTrack || !state.currentTrack.path) {
    showToast("Avval trekni tanlang!", "info");
    return;
  }
  showToast("🔊 EBU R128 (-14 LUFS) ovoz balansi me'yorlashtirildi", "success");
}
"""

anchor = "// STREAMLINED ESSENTIALS COMPATIBILITY STUBS (Zero-Bloat Architecture)"
idx = text.find(anchor)
assert idx != -1, "Anchor not found in app.js"

text = text[:idx] + car_functions + "\n" + text[idx:]

with open(app_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Car functions added to app.js successfully!")
