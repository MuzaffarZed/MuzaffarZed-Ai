from PIL import Image

img_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_synergy_masterpiece_verified.png"
im = Image.open(img_path)
print("Image dimensions:", im.size)

# Crop topbar controls
topbar = im.crop((240, 0, 1920, 160))
topbar.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_topbar_synergy.png")

# Crop category pills and cards
cards = im.crop((240, 160, 1920, 650))
cards.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_cards_synergy.png")

print("Cropped synergy screenshots successfully!")
