with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

c_idx = text.find('id="view-channel"')
if c_idx != -1:
    print("Channel section snippet:")
    print(text[c_idx:c_idx+500])

h_idx = text.find('id="view-history"')
if h_idx != -1:
    print("\nHistory section snippet:")
    print(text[h_idx:h_idx+400])
