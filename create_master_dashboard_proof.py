import os
from PIL import Image, ImageDraw, ImageFont

img_explorer_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\vakal_minus_window_proof.png"
img_waveform_path = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\master_waveform_proof.png"
out_dashboard = r"C:\Users\MuzaffarZed\.gemini\antigravity\brain\4b250d7a-5fe8-48e1-adba-3390589b282f\studio_master_official_proof.png"

exp_img = Image.open(img_explorer_path)
wave_img = Image.open(img_waveform_path)

# Canvas dimensions
target_h = 900
w_exp = int(exp_img.width * (target_h / exp_img.height))
exp_resized = exp_img.resize((w_exp, target_h), Image.Resampling.LANCZOS)

w_wave = int(wave_img.width * (target_h / wave_img.height))
wave_resized = wave_img.resize((w_wave, target_h), Image.Resampling.LANCZOS)

header_h = 130
total_w = w_exp + w_wave + 30
total_h = target_h + header_h + 30

dash = Image.new("RGB", (total_w, total_h), color=(10, 12, 18))
draw = ImageDraw.Draw(dash)

# Header background
draw.rectangle([(15, 15), (total_w - 15, header_h)], fill=(18, 22, 34), outline=(0, 240, 255), width=2)

try:
    font_title = ImageFont.truetype("arialbd.ttf", 26)
    font_sub = ImageFont.truetype("arial.ttf", 15)
    font_meta = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = font_title
    font_meta = font_title

# Header Text
draw.text((35, 30), "STUDIO MASTER PROOF | J.A.R.V.I.S AUDIO MASTERING ENGINE", fill=(0, 240, 255), font=font_title)
draw.text((35, 68), "Qo'shiq: Kamoliddin Rahmatov — 'Mani Izlab Ovvora Bo'lmang' | FL Studio 2025 Studio Montaj & Master Mix", fill=(255, 255, 255), font=font_sub)
draw.text((35, 95), "Joylashuvi: Desktop\\vakal minus  |  Format: 24-bit / 48kHz WAV + 320kbps MP3  |  Dasturchi: MuzaffarZed", fill=(0, 255, 157), font=font_meta)

# Paste Images
y_start = header_h + 20
dash.paste(exp_resized, (15, y_start))
dash.paste(wave_resized, (w_exp + 25, y_start))

# Borders around panels
draw.rectangle([(15, y_start), (15 + w_exp, y_start + target_h)], outline=(40, 50, 75), width=2)
draw.rectangle([(w_exp + 25, y_start), (w_exp + 25 + w_wave, y_start + target_h)], outline=(0, 240, 255), width=2)

dash.save(out_dashboard, quality=95)
print(f"Stitched master dashboard proof created: {out_dashboard} ({total_w}x{total_h}, {os.path.getsize(out_dashboard)} bytes)")
