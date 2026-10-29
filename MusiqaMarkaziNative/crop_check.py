from PIL import Image
import sys

img_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_desktop_streamlined_clean.png"
im = Image.open(img_path)
print("Image size:", im.size)

# Crop sidebar (left 300px)
sidebar = im.crop((0, 0, 320, 1080))
sidebar.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_sidebar_clean.png")

# Crop topbar and cockpit
topbar = im.crop((240, 0, 1920, 200))
topbar.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_topbar_clean.png")

print("Cropped successfully!")
