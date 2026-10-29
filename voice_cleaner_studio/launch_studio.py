import os
import webbrowser
import sys

def open_studio():
    html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
    if os.path.exists(html_path):
        print(f"Ochilyapti: {html_path}")
        webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")
    else:
        print("index.html topilmadi!")

if __name__ == "__main__":
    open_studio()
