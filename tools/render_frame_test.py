import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_frame(t, frame_idx, total_frames, font_path):
    W, H = 1080, 1920
    # 1. Base image
    img = Image.new("RGBA", (W, H), (6, 3, 14, 255))
    draw = ImageDraw.Draw(img)

    # 2. Nebula background gradient
    cx, cy = W // 2, 850
    # Create radial gradient on numpy
    y_coords, x_coords = np.ogrid[:H, :W]
    dist_from_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    max_r = 900
    nebula = np.clip(1.0 - dist_from_center / max_r, 0, 1)
    # Violet/Indigo/Teal tint
    r_ch = (nebula * 45).astype(np.uint8)
    g_ch = (nebula * 18).astype(np.uint8)
    b_ch = (nebula * 75).astype(np.uint8)
    bg_np = np.zeros((H, W, 4), dtype=np.uint8)
    bg_np[:, :, 0] = np.clip(6 + r_ch, 0, 255)
    bg_np[:, :, 1] = np.clip(3 + g_ch, 0, 255)
    bg_np[:, :, 2] = np.clip(14 + b_ch, 0, 255)
    bg_np[:, :, 3] = 255
    img = Image.fromarray(bg_np, "RGBA")
    draw = ImageDraw.Draw(img)

    # 3. Starfield with zoom motion
    np.random.seed(42) # fixed stars
    n_stars = 220
    base_x = np.random.uniform(-W, W, n_stars)
    base_y = np.random.uniform(-H, H, n_stars)
    base_z = np.random.uniform(0.1, 1.0, n_stars)
    # animate z
    z = (base_z - t * 0.12) % 1.0 + 0.05
    sx = (base_x / z + cx).astype(int)
    sy = (base_y / z + cy).astype(int)
    brightness = ((1.0 - z) * 255).astype(np.uint8)

    for i in range(n_stars):
        px, py, br = sx[i], sy[i], brightness[i]
        if 0 <= px < W and 0 <= py < H:
            rad = 1 if br < 180 else 2
            draw.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(br, br, 255, br))

    # 4. Accretion Disk & Black Hole (Gargantua Style)
    # Glow layer
    glow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)

    # Outer gravitational lens arc (top and bottom curved halos)
    rot = t * 45.0 # rotation degrees
    rot_rad = math.radians(rot)

    # Draw accretion disk back arc
    disk_rx = 340
    disk_ry = 95
    # Accretion outer glow
    for dr in range(50, 0, -5):
        alpha = int(45 * (1.0 - dr / 50))
        glow_draw.ellipse([cx - disk_rx - dr, cy - disk_ry - dr//3, cx + disk_rx + dr, cy + disk_ry + dr//3],
                          outline=(255, 140, 20, alpha), width=8)

    # Top Einstein lens arc
    glow_draw.arc([cx - 240, cy - 250, cx + 240, cy + 180], start=190, end=350, fill=(255, 180, 50, 220), width=16)
    # Bottom Einstein lens arc
    glow_draw.arc([cx - 220, cy - 160, cx + 220, cy + 240], start=10, end=170, fill=(255, 120, 20, 180), width=12)

    # Main disk ellipse (front)
    for w_i in range(12, 0, -2):
        col = (255, 230, 160, 240) if w_i <= 4 else (255, 120, 30, 160)
        glow_draw.ellipse([cx - disk_rx, cy - disk_ry, cx + disk_rx, cy + disk_ry], outline=col, width=w_i)

    # Event horizon (Black Sphere)
    bh_r = 145
    glow_draw.ellipse([cx - bh_r, cy - bh_r, cx + bh_r, cy + bh_r], fill=(0, 0, 0, 255))
    # Photon sphere bright boundary ring
    glow_draw.ellipse([cx - bh_r, cy - bh_r, cx + bh_r, cy + bh_r], outline=(255, 240, 200, 255), width=4)

    # Relativistic jets (vertical energy beams)
    beam_alpha = int(120 + 40 * math.sin(t * 8))
    jet_w = 12
    glow_draw.line([cx, cy - bh_r, cx, 0], fill=(120, 220, 255, beam_alpha), width=jet_w)
    glow_draw.line([cx, cy + bh_r, cx, H], fill=(120, 220, 255, beam_alpha), width=jet_w)

    # Composite glow
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)

    # 5. Top Header HUD
    # Progress Bar
    bar_w = int(W * (frame_idx / total_frames))
    draw.rectangle([0, 0, W, 8], fill=(30, 25, 45, 255))
    draw.rectangle([0, 0, bar_w, 8], fill=(255, 215, 0, 255))

    # Badge: KOINOTNING SIRLARI
    font_badge = ImageFont.truetype(font_path, 28)
    badge_text = "KOINOTNING ENG KATTA SIRI"
    bw = draw.textlength(badge_text, font=font_badge)
    bx0, by0 = (W - bw) // 2 - 24, 80
    bx1, by1 = (W + bw) // 2 + 24, 130
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=25, fill=(20, 12, 38, 200), outline=(0, 230, 255, 180), width=2)
    draw.text(((W - bw) // 2, 90), badge_text, font=font_badge, fill=(0, 240, 255, 255))

    # 6. Audio Waveform visualizer at y=1560
    n_bars = 36
    bar_spacing = 18
    total_w = n_bars * bar_spacing
    start_x = (W - total_w) // 2
    for b in range(n_bars):
        h_val = int(20 + 35 * math.sin(t * 12 + b * 0.4)**2 + 20 * math.cos(t * 6 + b * 0.7)**2)
        bx = start_x + b * bar_spacing
        draw.line([bx, 1580 - h_val, bx, 1580 + h_val], fill=(255, 215, 0, 220), width=4)

    # 7. Subtitles (Karaoke)
    font_sub = ImageFont.truetype(font_path, 54)
    # Example phrase: "Agar siz qora o'raga tushib ketsangiz,"
    words = [("Agar", False), ("siz", False), ("qora", True), ("o'raga", False), ("tushib ketsangiz,", False)]
    total_text_w = sum(draw.textlength(w[0] + " ", font=font_sub) for w in words)
    cur_x = (W - total_text_w) // 2
    sub_y = 1380

    for word, is_active in words:
        w_len = draw.textlength(word + " ", font=font_sub)
        if is_active:
            # Highlight with gold color and slight glow background
            draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 230, 0, 255),
                      stroke_width=5, stroke_fill=(0, 0, 0, 255))
        else:
            # Crisp white
            draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 255, 255, 230),
                      stroke_width=4, stroke_fill=(0, 0, 0, 255))
        cur_x += w_len

    # 8. Sleek Watermark (Rule 7: Dasturchi: MuzaffarZed)
    font_wm = ImageFont.truetype(font_path, 26)
    wm_text = "Dasturchi: MuzaffarZed"
    wm_w = draw.textlength(wm_text, font=font_wm)
    draw.text(((W - wm_w) // 2, 1840), wm_text, font=font_wm, fill=(180, 180, 200, 140))

    return img.convert("RGB")

if __name__ == "__main__":
    font_path = r"C:\Users\MuzaffarZed\ai_workspace\tools\fonts\Inter-Black.ttf"
    test_img = create_frame(2.0, 60, 306, font_path)
    out_png = r"C:\Users\MuzaffarZed\ai_workspace\tools\test_frame.png"
    test_img.save(out_png)
    print("Test frame saved to:", out_png)
