from PIL import Image
import numpy as np

im = Image.open(r"C:\Users\MuzaffarZed\ai_workspace\tools\current_screen2.png").convert("RGB")
arr = np.array(im)

# Look for the bookmark icon or the white text 'Избранное'
# In the drawer, the background is dark grey/blue ~ (24, 37, 51)
# Let's inspect rows around y=500 to 650, x=350 to 550
# Find where the text is brightest white
for y in range(400, 700, 20):
    row = arr[y, 350:550]
    bright_pixels = np.sum(row > 200)
    print(f"y={y}: bright pixels={bright_pixels}")
