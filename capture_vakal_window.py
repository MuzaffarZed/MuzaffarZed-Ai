import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))

from bridge.windows_controller import get_windows_controller

controller = get_windows_controller()
img = controller.capture_window("vakal minus")

if img:
    out_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\vakal_minus_window_proof.png"
    img.save(out_path)
    print(f"Captured vakal minus window! Saved to: {out_path} ({img.size[0]}x{img.size[1]})")
else:
    print("Could not capture vakal minus window.")
