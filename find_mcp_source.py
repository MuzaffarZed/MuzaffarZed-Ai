import os

def find_file():
    paths = [
        r"C:\Users\MuzaffarZed\.gemini\antigravity",
        r"C:\Users\MuzaffarZed\.gemini",
        r"C:\Users\MuzaffarZed\ai_workspace",
        r"C:\Users\MuzaffarZed\AppData\Roaming",
        r"C:\Users\MuzaffarZed\AppData\Local"
    ]
    for p in paths:
        if not os.path.exists(p): continue
        for root, dirs, files in os.walk(p):
            if any(skip in root for skip in ['node_modules', '.git', 'venv', '__pycache__', 'site-packages']):
                continue
            for f in files:
                if f.endswith('.py') and ('jarvis' in f or 'windows' in f or 'mcp' in f):
                    fp = os.path.join(root, f)
                    try:
                        c = open(fp, 'r', encoding='utf-8', errors='ignore').read()
                        if 'windows_focus_window' in c:
                            print("FOUND:", fp)
                    except:
                        pass

find_file()
