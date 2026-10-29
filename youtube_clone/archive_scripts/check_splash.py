with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

print("triggerCenterSplash in app.js:", "triggerCenterSplash" in text)
print("initScrubBufferAndTooltip in app.js:", "initScrubBufferAndTooltip" in text)
