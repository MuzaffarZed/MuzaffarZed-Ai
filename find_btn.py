from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\MuzaffarZed\ai_workspace\telegram_appeal_start2.png")
arr = np.array(img)

# Search for the white text in the 4 buttons (y from 630 to 860, x from 900 to 1400)
# Button 4 is near the bottom
sub = arr[800:860, 950:1350]
mask = (sub[:, :, 0] > 200) & (sub[:, :, 1] > 200) & (sub[:, :, 2] > 200)
ys, xs = np.where(mask)
if len(xs) > 0:
    print(f"Center: x={950 + int(np.mean(xs))}, y={800 + int(np.mean(ys))}")
    print(f"Y min={800 + ys.min()}, max={800 + ys.max()}")
else:
    print("None found")
