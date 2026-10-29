with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('renderComments(video) {')
end_idx = text.find('renderRelatedVideos(', idx)
print(text[idx:end_idx].encode('ascii', errors='replace').decode('ascii'))
