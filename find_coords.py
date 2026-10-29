from PIL import Image
import numpy as np

im = Image.open('C:/Users/MuzaffarZed/ai_workspace/crop_settings_menu.png').convert('RGB')
arr = np.array(im)
# Find white pixels (text) in the top 50 pixels of this crop
mask = (arr[:60, :, 0] > 180) & (arr[:60, :, 1] > 180) & (arr[:60, :, 2] > 180)
y_s, x_s = np.where(mask)
print(f"Settings text x in [{x_s.min()}, {x_s.max()}], y in [{y_s.min()}, {y_s.max()}]")
crop_cx = (x_s.min() + x_s.max()) // 2
crop_cy = (y_s.min() + y_s.max()) // 2
abs_x = 1050 + crop_cx
abs_y = 40 + crop_cy
print(f"Settings center: Absolute({abs_x}, {abs_y})")
