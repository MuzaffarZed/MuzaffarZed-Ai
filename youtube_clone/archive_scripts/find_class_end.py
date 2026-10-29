with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

end_idx = text.rfind('  window.addEventListener')
print("End of class is before window.addEventListener at:", end_idx)
print(repr(text[end_idx-300:end_idx]))
