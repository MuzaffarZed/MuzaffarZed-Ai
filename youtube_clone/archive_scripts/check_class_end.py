with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind("  }\n\n  // Initialize")
if idx == -1:
    idx = text.rfind("  }\n\n  window.")
if idx == -1:
    idx = text.rfind("  }\n})();")

print("Target location found at:", idx)
print(text[idx-300:idx+150].encode('ascii', errors='replace').decode('ascii'))
