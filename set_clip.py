import sys
import subprocess

def set_clipboard(text):
    p = subprocess.Popen(['powershell', '-NoProfile', '-NonInteractive', '-Command', '$input | Set-Clipboard'], stdin=subprocess.PIPE, text=True, encoding='utf-8')
    p.communicate(input=text)

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else '[01] MuzaffarZed AI & Bot Loyihalari'
    set_clipboard(text)
    print("Clipboard updated to:", text)
