import sys, os
sys.stdout.reconfigure(encoding='utf-8')

test_path = r"C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\test_pro.py"

with open(test_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "def test_reels_and_dj_and_jarvis_ui" in l:
        print("Found at line:", i+1)
        for j in range(i, min(i+45, len(lines))):
            print(f"{j+1}: {repr(lines[j])}")
        break
