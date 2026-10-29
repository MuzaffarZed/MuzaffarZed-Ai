import re

with open(r'C:\Users\MuzaffarZed\Documents\Image-Line\FL Studio\Projects\Backup\untitled (autosaved at 16h39).flp', 'rb') as f:
    data = f.read()

# Look for occurrences of 'lmang karaoke' in the file
idx = 0
while True:
    pos = data.find(b'lmang karaoke', idx)
    if pos == -1:
        break
    print(f"Found 'lmang karaoke' at offset {pos} (0x{pos:X})")
    # print 64 bytes before and after
    start = max(0, pos - 40)
    end = min(len(data), pos + 80)
    print("  Context:", data[start:end])
    idx = pos + 1
