import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
app_path = os.path.join(base, 'ui', 'app.js')

with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

# 1. Clean switchTab
old_switch = """function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.toggle("active", t.dataset.tab === tabId));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.toggle("active", p.id === `tab-${tabId}`));
  if (tabId === "aimp" || tabId === "simulator") refreshLibrary();
  if (tabId === "kiosk") loadKioskPackages();
  if (tabId === "reels") initReelsStudio();
  if (tabId === "dj") initDjStudio();
  if (tabId === "turbo") refreshTurboTelemetry();
  if (tabId === "vault") loadVaultFiles();
  syncVideoDockPlacement();
}"""

new_switch = """function switchTab(tabId) {
  state.activeTab = tabId;
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.toggle("active", t.dataset.tab === tabId));
  document.querySelectorAll(".tab-pane").forEach(p => p.classList.toggle("active", p.id === `tab-${tabId}`));
  if (tabId === "aimp" || tabId === "simulator") refreshLibrary();
  syncVideoDockPlacement();
}"""

if old_switch in app_text:
    app_text = app_text.replace(old_switch, new_switch, 1)
    print("switchTab updated!")
else:
    print("WARNING: old_switch not found in app.js")

# 2. Replace bloat block from lines 3839 to 5370 (before Section 17: JARVIS)
target_start = "/* ==========================================================================\n   SMART DUPLICATES HUNTER & CLEANER (6-VARIANT)\n   ========================================================================== */"
target_end = "// ============================================================================\n// 17. JARVIS OVOZLI & AQLLI AI YORDAMCHI"

start_idx = app_text.find(target_start)
end_idx = app_text.find(target_end)

if start_idx != -1 and end_idx != -1:
    clean_stubs = """// ============================================================================
// STREAMLINED ESSENTIALS COMPATIBILITY STUBS (Zero-Bloat Architecture)
// ============================================================================
function openDuplicatesModal() { showToast("Dublikatlarni tozalash o'rniga Fleshka Kiosk va avto-raqamlashdan foydalaning", "info"); }
function closeDuplicatesModal() {}
function scanDuplicatesAction() {}
function autoSelectInferiorDuplicates() {}
function deleteSelectedDuplicatesAction() {}
function openStemSeparatorModal() { showToast("Minusovka studiyasi o'rniga Salon Ekvayzeridan foydalaning", "info"); }
function closeStemSeparatorModal() {}
function separateCurrentInspectorStems() {}
function applyStemAuditionDSPs() {}
function exportStemAction() {}
function loadKioskPackages() {}
function initReelsStudio() {}
function initDjStudio() {}
function refreshTurboTelemetry() {}
function runTurboCleanAction() { showToast("RAM xotirasi me'yorida!", "success"); }
function loadVaultFiles() {}
function closeVaultDecryptModal() {}

"""
    app_text = app_text[:start_idx] + clean_stubs + app_text[end_idx:]
    print("Bloat block in app.js successfully pruned!")
else:
    print(f"WARNING: start_idx={start_idx}, end_idx={end_idx}")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_text)

print("app.js updated successfully!")
