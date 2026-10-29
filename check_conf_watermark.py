import re

conf_path = r"D:\KANPIYUTER O'YINLARI\FlatOut2\dgVoodoo.conf"
with open(conf_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

for line in content.splitlines():
    if 'watermark' in line.lower():
        print(line)
