import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_gargantua_frame(t, frame_idx, total_frames, font_path, subtitle_words=None):
    W, H = 1080, 1920
    cx, cy = W // 2, 820

    # 1. Cosmic Background with Deep Nebula Clouds
    y_coords, x_coords = np.ogrid[:H, :W]
    d_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    
    # Swirling nebula texture
    angle = np.arctan2(y_coords - cy, x_coords - cx)
    spiral = np.sin(d_center * 0.008 - angle * 2.0 - t * 0.8)
    nebula_intensity = np.clip((1.0 - d_center / 1050.0) * (0.6 + 0.4 * spiral), 0, 1)

    r_ch = (nebula_intensity * 60 + 10).astype(np.uint8)
    g_ch = (nebula_intensity * 25 + 5).astype(np.uint8)
    b_ch = (nebula_intensity * 95 + 20).astype(np.uint8)
    
    bg_np = np.zeros((H, W, 4), dtype=np.uint8)
    bg_np[:, :, 0] = r_ch
    bg_np[:, :, 1] = g_ch
    bg_np[:, :, 2] = b_ch
    bg_np[:, :, 3] = 255
    img = Image.fromarray(bg_np, "RGBA")

    # 2. 3D Warp Starfield
    star_draw = ImageDraw.Draw(img)
    np.random.seed(1337)
    n_stars = 260
    bx = np.random.uniform(-W, W, n_stars)
    by = np.random.uniform(-H, H, n_stars)
    bz = np.random.uniform(0.05, 1.0, n_stars)
    # Fly forward
    z = (bz - t * 0.08) % 1.0 + 0.05
    sx = (bx / z + cx).astype(int)
    sy = (by / z + cy).astype(int)
    br = ((1.0 - z) * 255).astype(np.uint8)

    for i in range(n_stars):
        px, py, b_val = sx[i], sy[i], br[i]
        if 0 <= px < W and 0 <= py < H:
            rad = 1 if b_val < 160 else (2 if b_val < 220 else 3)
            star_draw.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(b_val, b_val, 255, b_val))

    # 3. Accretion Disk (Multi-layer Luminous Plasma & Gravitational Lensing)
    plasma_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(plasma_layer)

    # Top gravitational lensing arch (light bent around back of black hole)
    # Radiates above the horizon
    for i in range(24, 0, -2):
        alpha = int(120 * (1.0 - i / 24))
        pdraw.arc([cx - 260 - i, cy - 300 - i, cx + 260 + i, cy + 180 + i],
                  start=185, end=355, fill=(255, 150 + i*4, 40, alpha), width=6)
    # Bright inner lens ridge
    pdraw.arc([cx - 240, cy - 280, cx + 240, cy + 160], start=190, end=350, fill=(255, 240, 200, 230), width=8)

    # Bottom lens reflection arc
    for i in range(16, 0, -2):
        alpha = int(80 * (1.0 - i / 16))
        pdraw.arc([cx - 220 - i, cy - 140 - i, cx + 220 + i, cy + 280 + i],
                  start=10, end=170, fill=(255, 120, 20, alpha), width=6)
    pdraw.arc([cx - 210, cy - 130, cx + 210, cy + 260], start=15, end=165, fill=(255, 200, 100, 180), width=6)

    # Equatorial Accretion Disk (Front & Behind)
    disk_w = 420
    disk_h = 110
    # Outer fiery haze
    for dr in range(60, 0, -6):
        a = int(60 * (1.0 - dr / 60))
        pdraw.ellipse([cx - disk_w - dr, cy - disk_h - dr//3, cx + disk_w + dr, cy + disk_h + dr//3],
                      outline=(255, 100, 20, a), width=8)

    # Dense glowing plasma rings
    for r_idx in range(10):
        w_factor = disk_w - r_idx * 15
        h_factor = disk_h - r_idx * 4
        # Doppler beaming: Left side approaching observer is brighter/hotter (blue/white-shifted), right side receding is redder!
        pdraw.arc([cx - w_factor, cy - h_factor, cx + w_factor, cy + h_factor],
                  start=120, end=260, fill=(255, 255, 240, 220), width=7) # Bright hot approaching side!
        pdraw.arc([cx - w_factor, cy - h_factor, cx + w_factor, cy + h_factor],
                  start=260, end=380, fill=(255, 160, 40, 180), width=6)
        pdraw.arc([cx - w_factor, cy - h_factor, cx + w_factor, cy + h_factor],
                  start=20, end=120, fill=(255, 110, 20, 150), width=6)

    # Swirling accretion particles
    np.random.seed(999)
    n_particles = 140
    p_radii = np.random.uniform(160, 440, n_particles)
    p_base_angles = np.random.uniform(0, 2 * np.pi, n_particles)
    p_speeds = 180.0 / p_radii # Keplerian speed (closer rotates faster!)
    p_cur_angles = p_base_angles + p_speeds * t * 2.0

    px_coords = cx + p_radii * np.cos(p_cur_angles)
    py_coords = cy + (p_radii * 0.28) * np.sin(p_cur_angles)
    for p_i in range(n_particles):
        px = int(px_coords[p_i])
        py = int(py_coords[p_i])
        prad = np.random.randint(2, 5)
        # Hot white/yellow/orange color
        p_col = (255, 250, 200, 220) if p_radii[p_i] < 260 else (255, 160, 50, 180)
        pdraw.ellipse([px - prad, py - prad, px + prad, py + prad], fill=p_col)

    # Apply soft glow to plasma layer
    plasma_blur = plasma_layer.filter(ImageFilter.GaussianBlur(radius=6))
    img = Image.alpha_composite(img, plasma_blur)
    img = Image.alpha_composite(img, plasma_layer)

    # 4. Singularity / Event Horizon (Black Sphere with Photon Halo)
    bh_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bh_draw = ImageDraw.Draw(bh_layer)
    bh_r = 150

    # Photon Ring (Super-heated photon shell on the edge)
    for pr in range(12, 0, -2):
        bh_draw.ellipse([cx - bh_r - pr, cy - bh_r - pr, cx + bh_r + pr, cy + bh_r + pr],
                        outline=(255, 230, 120, int(200 * (1.0 - pr / 12))), width=3)
    bh_draw.ellipse([cx - bh_r, cy - bh_r, cx + bh_r, cy + bh_r],
                    outline=(255, 255, 240, 255), width=4)

    # Absolute darkness inside event horizon
    bh_draw.ellipse([cx - bh_r + 2, cy - bh_r + 2, cx + bh_r - 2, cy + bh_r - 2],
                    fill=(0, 0, 0, 255))

    # Polar Relativistic Jets (Shooting OUTWARD from top and bottom, NOT through black hole!)
    jet_len = 700
    for j in range(20):
        spread = j * 0.8
        j_alpha = int(140 * (1.0 - j / 20) * (0.8 + 0.2 * math.sin(t * 10 + j)))
        # Top jet (shoots from top pole cy - bh_r upwards to 0)
        bh_draw.polygon([
            (cx - 10 - spread, cy - bh_r + 5),
            (cx + 10 + spread, cy - bh_r + 5),
            (cx + 35 + spread*2, cy - bh_r - jet_len),
            (cx - 35 - spread*2, cy - bh_r - jet_len)
        ], fill=(0, 220, 255, j_alpha))
        # Bottom jet (shoots from bottom pole cy + bh_r downwards to H)
        bh_draw.polygon([
            (cx - 10 - spread, cy + bh_r - 5),
            (cx + 10 + spread, cy + bh_r - 5),
            (cx + 35 + spread*2, cy + bh_r + jet_len),
            (cx - 35 - spread*2, cy + bh_r + jet_len)
        ], fill=(0, 220, 255, j_alpha))

    # Composite Black Hole & Jets
    img = Image.alpha_composite(img, bh_layer)
    draw = ImageDraw.Draw(img)

    # 5. Top Cinematic HUD & Progress Bar
    bar_w = int(W * (frame_idx / total_frames))
    draw.rectangle([0, 0, W, 8], fill=(30, 20, 45, 255))
    draw.rectangle([0, 0, bar_w, 8], fill=(255, 215, 0, 255))

    # Glowing Badge: 🌌 KOINOTNING SIRLARI
    font_badge = ImageFont.truetype(font_path, 30)
    badge_text = "KOINOTNING ENG KATTA SIRI"
    bw = draw.textlength(badge_text, font=font_badge)
    bx0, by0 = (W - bw) // 2 - 28, 90
    bx1, by1 = (W + bw) // 2 + 28, 148
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=28, fill=(18, 10, 36, 220), outline=(0, 240, 255, 200), width=3)
    draw.text(((W - bw) // 2, 102), badge_text, font=font_badge, fill=(0, 245, 255, 255))

    # 6. Sleek Audio Waveform Visualizer (at y = 1180)
    n_bars = 42
    bar_w_unit = 16
    start_x = (W - n_bars * bar_w_unit) // 2
    for b in range(n_bars):
        # dynamic wave reaction
        h_val = int(14 + 32 * math.sin(t * 14 + b * 0.35)**2 + 18 * math.cos(t * 8 + b * 0.6)**2)
        bx = start_x + b * bar_w_unit
        # Gradient bar color from cyan to gold
        bar_color = (int(0 + 255 * (b / n_bars)), int(240 - 25 * (b / n_bars)), int(255 - 255 * (b / n_bars)), 230)
        draw.line([bx, 1180 - h_val, bx, 1180 + h_val], fill=bar_color, width=5)

    # 7. Dynamic Karaoke Subtitles (Inter Black font)
    if subtitle_words:
        font_sub = ImageFont.truetype(font_path, 54)
        sub_y = 1380
        total_w = sum(draw.textlength(w[0] + " ", font=font_sub) for w in subtitle_words)
        cur_x = (W - total_w) // 2

        # Subtitle dark backplate for readability
        pad_x = 35
        pad_y = 20
        draw.rounded_rectangle(
            [cur_x - pad_x, sub_y - pad_y, cur_x + total_w + pad_x, sub_y + 70 + pad_y],
            radius=20, fill=(5, 3, 12, 190), outline=(255, 215, 0, 100), width=2
        )

        for word, is_active in subtitle_words:
            w_len = draw.textlength(word + " ", font=font_sub)
            if is_active:
                # Active word: Neon Gold highlight with scale effect
                draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 235, 0, 255),
                          stroke_width=6, stroke_fill=(0, 0, 0, 255))
            else:
                # Inactive word: Crisp clean white
                draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 255, 255, 220),
                          stroke_width=4, stroke_fill=(0, 0, 0, 255))
            cur_x += w_len

    # 8. Discrete Author Signature (Rule 7: Dasturchi: MuzaffarZed)
    font_wm = ImageFont.truetype(font_path, 26)
    wm_text = "Dasturchi: MuzaffarZed"
    wm_w = draw.textlength(wm_text, font=font_wm)
    draw.text(((W - wm_w) // 2, 1840), wm_text, font=font_wm, fill=(200, 200, 220, 150))

    return img.convert("RGB")

if __name__ == "__main__":
    font_path = r"C:\Users\MuzaffarZed\ai_workspace\tools\fonts\Inter-Black.ttf"
    sub_words = [("Agar", False), ("siz", False), ("qora", True), ("o'raga", False), ("tushib ketsangiz,", False)]
    test_img = create_gargantua_frame(2.5, 75, 306, font_path, sub_words)
    out_png = r"C:\Users\MuzaffarZed\ai_workspace\tools\test_frame_v2.png"
    test_img.save(out_png)
    print("Saved test_frame_v2.png successfully!")
