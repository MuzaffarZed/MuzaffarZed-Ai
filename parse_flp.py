import pyflp
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

flp_paths = [
    os.path.expanduser(r"~\Documents\Image-Line\FL Studio\Projects\Backup\untitled (autosaved at 16h39).flp"),
    r"C:\Users\MuzaffarZed\Desktop\vakal minus\Mani_Izlab_Ovvora_Bolmang_Studio_Project.flp"
]

for p in flp_paths:
    if os.path.exists(p):
        print(f"Reading FLP: {p}")
        try:
            project = pyflp.parse(p)
            print("Project title:", project.title)
            print("BPM (Tempo):", project.tempo)
            print("Arrangements count:", len(project.arrangements))
            for arr in project.arrangements:
                print("Arrangement tracks count:", len(arr.tracks))
                for t in arr.tracks:
                    if len(t) > 0:
                        print(f"  Track {t.name}: {len(t)} items")
                        for item in t:
                            print(f"    Item position: {item.position}, length: {item.length}")
        except Exception as e:
            print(f"Error parsing {p}: {e}")
