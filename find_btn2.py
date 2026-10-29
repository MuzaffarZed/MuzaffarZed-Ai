from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\MuzaffarZed\ai_workspace\telegram_appeal_prompt_text.png")
arr = np.array(img)

# Search for the button 'Нет, ничего подобного не было.'
# The button itself has dark background ~ [36, 47, 61], but around it is darker [23, 33, 43]
# The text has white pixels
sub = arr[750:810, 950:1400]
mask = (sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)
ys, xs = np.where(mask)
if len(xs) > 0:
    print(f"Text center: x={950 + int(np.mean(xs))}, y={750 + int(np.mean(ys))}")
    print(f"X range: [{950+xs.min()}, {950+xs.max()}], Y range: [{750+ys.min()}, {750+ys.max()}]")
