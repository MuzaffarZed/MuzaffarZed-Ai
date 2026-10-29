import os

lnk_path = r"C:\Users\MuzaffarZed\Desktop\Telegram Desktop.lnk"
with open(lnk_path, "rb") as f:
    data = f.read()

text_utf16 = data.decode("utf-16le", errors="ignore")
text_utf8 = data.decode("utf-8", errors="ignore")

for line in (text_utf16 + "\n" + text_utf8).split("\x00"):
    line = "".join(c for c in line if 32 <= ord(c) <= 126)
    if any(k in line.lower() for k in ["telegram", ".exe", "users"]):
        print("Match:", line)
