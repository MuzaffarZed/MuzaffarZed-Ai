from PIL import Image

img_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_desktop_streamlined_clean.png"
im = Image.open(img_path)

# Crop cards area
cards = im.crop((240, 180, 1920, 850))
cards.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_cards_clean.png")

# Crop bottom playback deck
deck = im.crop((0, 850, 1920, 1080))
deck.save(r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\2f3e54a9-40f9-472c-8160-446093bb35d0\live_bottom_deck_clean.png")

print("Cards and deck cropped!")
