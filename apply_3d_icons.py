import os
from PIL import Image, ImageDraw

src_img_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\savdopro_3d_icon_1791664640653.jpg"
android_res = r"C:\Users\MuzaffarZed\ai_workspace\flowwise_android\app\src\main\res"

sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

img = Image.open(src_img_path).convert("RGBA")

def create_round_icon(image, size):
    resized = image.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    rounded = Image.new("RGBA", (size, size))
    rounded.paste(resized, (0, 0), mask)
    return rounded

for folder, size in sizes.items():
    dest_dir = os.path.join(android_res, folder)
    os.makedirs(dest_dir, exist_ok=True)
    
    # Square / standard icon
    resized = img.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(os.path.join(dest_dir, "ic_launcher.png"), "PNG")
    
    # Round icon
    round_img = create_round_icon(img, size)
    round_img.save(os.path.join(dest_dir, "ic_launcher_round.png"), "PNG")

# Also save high-res 512x512
hires_dir = os.path.join(android_res, "drawable")
os.makedirs(hires_dir, exist_ok=True)
img.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(hires_dir, "savdopro_icon_512.png"), "PNG")

# Also save to public in zafaruzb-main
public_dir = r"C:\Users\MuzaffarZed\ai_workspace\zafaruzb-main\public"
os.makedirs(public_dir, exist_ok=True)
img.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(public_dir, "savdopro_logo.png"), "PNG")
img.resize((64, 64), Image.Resampling.LANCZOS).save(os.path.join(public_dir, "favicon.png"), "PNG")

print("All SavdoPro 3D icons applied successfully!")
