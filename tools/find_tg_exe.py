import os

search_roots = [
    r"C:\Users\MuzaffarZed",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
]

found = []
for root_dir in search_roots:
    for root, dirs, files in os.walk(root_dir):
        if "Telegram.exe" in files:
            p = os.path.join(root, "Telegram.exe")
            print("Found Telegram.exe:", p)
            found.append(p)
        # Avoid traversing huge non-program folders
        if root_dir == r"C:\Users\MuzaffarZed":
            dirs[:] = [d for d in dirs if d in ["AppData", "Desktop", "Downloads", "Programs", "Local", "Roaming", "Telegram Desktop"]]

print("Total found:", len(found))
