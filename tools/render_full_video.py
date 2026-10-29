import os
import sys
import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Phrases & Word Timings
PHRASES = [
    {
        "start": 0.0, "end": 1.05,
        "words": [
            ("Tasavvur", 0.0, 0.45),
            ("qiling:", 0.45, 1.05)
        ]
    },
    {
        "start": 1.10, "end": 3.15,
        "words": [
            ("Agar", 1.10, 1.55),
            ("siz", 1.55, 1.84),
            ("qora", 1.84, 2.26),
            ("o'raga", 2.26, 2.62),
            ("tushib ketsangiz,", 2.62, 3.15)
        ]
    },
    {
        "start": 3.25, "end": 4.85,
        "words": [
            ("siz", 3.25, 3.45),
            ("uchun", 3.45, 3.72),
            ("vaqt", 3.72, 4.10),
            ("butunlay", 4.10, 4.45),
            ("to'xtaydi!", 4.45, 4.85)
        ]
    },
    {
        "start": 4.90, "end": 6.55,
        "words": [
            ("Tashqi", 4.90, 5.30),
            ("dunyoda", 5.30, 5.60),
            ("esa", 5.60, 5.82),
            ("millionlab", 5.82, 6.20),
            ("yillar", 6.20, 6.55)
        ]
    },
    {
        "start": 6.65, "end": 8.05,
        "words": [
            ("bir", 6.65, 7.00),
            ("soniyada", 7.00, 7.36),
            ("o'tib", 7.36, 7.65),
            ("ketadi.", 7.65, 8.05)
        ]
    },
    {
        "start": 8.10, "end": 10.18,
        "words": [
            ("Bu —", 8.10, 8.35),
            ("koinotning", 8.35, 8.86),
            ("eng", 8.86, 9.15),
            ("sirli", 9.15, 9.45),
            ("mo'jizasidir!", 9.45, 10.18)
        ]
    }
]

def get_current_subtitle(t):
    for phrase in PHRASES:
        if phrase["start"] <= t <= phrase["end"] + 0.15:
            words_status = []
            for w, s, e in phrase["words"]:
                is_active = (s <= t <= e)
                words_status.append((w, is_active))
            return words_status
    return None

def main():
    W, H = 1080, 1920
    FPS = 30
    cx, cy = W // 2, 820
    audio_path = r"C:\Users\MuzaffarZed\ai_workspace\tools\final_audio.wav"
    output_video = r"C:\Users\MuzaffarZed\ai_workspace\qiziqarli_video.mp4"
    font_path = r"C:\Users\MuzaffarZed\ai_workspace\tools\fonts\Inter-Black.ttf"

    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path]
    total_dur = float(subprocess.check_output(dur_cmd).strip())
    total_frames = int(total_dur * FPS)
    print(f"Blazing fast render: {total_frames} frames ({total_dur:.2f}s) at {FPS} FPS...")

    # Load audio volume envelope for waveform reaction
    from scipy.io import wavfile
    rate, data = wavfile.read(audio_path)
    if data.ndim > 1:
        data = data.mean(axis=1)
    abs_data = np.abs(data.astype(np.float32))
    chunk_size = int(rate / FPS)
    envelope = [np.mean(abs_data[i*chunk_size:(i+1)*chunk_size]) for i in range(total_frames + 5)]
    max_env = max(envelope) if max(envelope) > 0 else 1.0
    envelope = [e / max_env for e in envelope]

    # Pre-render static base nebula ONCE
    print("Pre-rendering static cosmic background...")
    y_coords, x_coords = np.ogrid[:H, :W]
    d_center = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    nebula_int = np.clip((1.0 - d_center / 1100.0) * 0.85, 0, 1)
    bg_np = np.zeros((H, W, 4), dtype=np.uint8)
    bg_np[:, :, 0] = (nebula_int * 60 + 8).astype(np.uint8)
    bg_np[:, :, 1] = (nebula_int * 24 + 4).astype(np.uint8)
    bg_np[:, :, 2] = (nebula_int * 95 + 18).astype(np.uint8)
    bg_np[:, :, 3] = 255
    static_bg_img = Image.fromarray(bg_np, "RGBA")

    # Pre-generate stars
    np.random.seed(2026)
    n_stars = 260
    bx = np.random.uniform(-W, W, n_stars)
    by = np.random.uniform(-H, H, n_stars)
    bz = np.random.uniform(0.05, 1.0, n_stars)

    # Pre-generate accretion particles
    n_particles = 140
    p_radii = np.random.uniform(165, 430, n_particles)
    p_base_angles = np.random.uniform(0, 2 * math.pi, n_particles)
    p_speeds = 160.0 / p_radii

    # Fonts
    font_badge = ImageFont.truetype(font_path, 30)
    font_sub = ImageFont.truetype(font_path, 48)
    font_wm = ImageFont.truetype(font_path, 26)

    # Pre-calculate badge dimensions
    temp_draw = ImageDraw.Draw(static_bg_img)
    badge_text = "KOINOTNING ENG KATTA SIRI"
    bw = temp_draw.textlength(badge_text, font=font_badge)
    bx0, by0 = (W - bw) // 2 - 28, 90
    bx1, by1 = (W + bw) // 2 + 28, 148

    wm_text = "Dasturchi: MuzaffarZed"
    wm_w = temp_draw.textlength(wm_text, font=font_wm)
    wm_x = (W - wm_w) // 2

    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_video
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    for frame_idx in range(total_frames):
        t = frame_idx / FPS
        env_val = envelope[frame_idx] if frame_idx < len(envelope) else 0.2

        # Copy static base image
        img = static_bg_img.copy()
        draw = ImageDraw.Draw(img)

        # 1. Warp Stars
        z = (bz - t * 0.08) % 1.0 + 0.05
        sx = (bx / z + cx).astype(int)
        sy = (by / z + cy).astype(int)
        br = ((1.0 - z) * 255).astype(np.uint8)

        for i in range(n_stars):
            px, py, b_val = sx[i], sy[i], br[i]
            if 0 <= px < W and 0 <= py < H:
                rad = 1 if b_val < 160 else (2 if b_val < 220 else 3)
                draw.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(b_val, b_val, 255, b_val))

        # 2. Accretion Disk & Gravitational Lens
        # Top Einstein Arch (behind black hole)
        for i in range(18, 0, -3):
            alpha = int(120 * (1.0 - i / 18))
            draw.arc([cx - 260 - i, cy - 300 - i, cx + 260 + i, cy + 180 + i],
                     start=185, end=355, fill=(255, 150 + i*4, 40, alpha), width=5)
        draw.arc([cx - 240, cy - 280, cx + 240, cy + 160], start=190, end=350, fill=(255, 240, 200, 240), width=8)

        # Bottom Reflection Arch
        for i in range(14, 0, -3):
            alpha = int(80 * (1.0 - i / 14))
            draw.arc([cx - 220 - i, cy - 140 - i, cx + 220 + i, cy + 280 + i],
                     start=10, end=170, fill=(255, 120, 20, alpha), width=5)
        draw.arc([cx - 210, cy - 130, cx + 210, cy + 260], start=15, end=165, fill=(255, 200, 100, 200), width=6)

        # Main Equatorial Disk
        disk_w = 420
        disk_h = 110
        for dr in range(48, 0, -6):
            a = int(60 * (1.0 - dr / 48))
            draw.ellipse([cx - disk_w - dr, cy - disk_h - dr//3, cx + disk_w + dr, cy + disk_h + dr//3],
                         outline=(255, 100, 20, a), width=7)

        # Beaming plasma rings (Left side is brighter approaching side)
        for r_idx in range(8):
            wf = disk_w - r_idx * 16
            hf = disk_h - r_idx * 4
            draw.arc([cx - wf, cy - hf, cx + wf, cy + hf],
                     start=120, end=260, fill=(255, 255, 240, 230), width=6)
            draw.arc([cx - wf, cy - hf, cx + wf, cy + hf],
                     start=260, end=380, fill=(255, 160, 40, 190), width=5)
            draw.arc([cx - wf, cy - hf, cx + wf, cy + hf],
                     start=20, end=120, fill=(255, 110, 20, 160), width=5)

        # Orbiting particles
        cur_angles = p_base_angles + p_speeds * t * 2.2
        px_coords = cx + p_radii * np.cos(cur_angles)
        py_coords = cy + (p_radii * 0.28) * np.sin(cur_angles)
        for p_i in range(n_particles):
            px_p = int(px_coords[p_i])
            py_p = int(py_coords[p_i])
            prad = 2 if p_radii[p_i] > 300 else 3
            p_col = (255, 250, 200, 220) if p_radii[p_i] < 260 else (255, 160, 50, 190)
            draw.ellipse([px_p - prad, py_p - prad, px_p + prad, py_p + prad], fill=p_col)

        # 3. Singularity / Event Horizon
        bh_r = 150
        # Glowing photon ring
        for pr in range(10, 0, -2):
            draw.ellipse([cx - bh_r - pr, cy - bh_r - pr, cx + bh_r + pr, cy + bh_r + pr],
                         outline=(255, 230, 120, int(200 * (1.0 - pr / 10))), width=3)
        draw.ellipse([cx - bh_r, cy - bh_r, cx + bh_r, cy + bh_r], outline=(255, 255, 240, 255), width=4)
        # Event horizon black core
        draw.ellipse([cx - bh_r + 2, cy - bh_r + 2, cx + bh_r - 2, cy + bh_r - 2], fill=(0, 0, 0, 255))

        # Polar jets (shooting outward)
        jet_len = 720
        for j in range(14):
            spread = j * 0.8
            j_alpha = int(140 * (1.0 - j / 14) * (0.8 + 0.2 * math.sin(t * 10 + j)))
            draw.polygon([
                (cx - 10 - spread, cy - bh_r + 5), (cx + 10 + spread, cy - bh_r + 5),
                (cx + 35 + spread*2, cy - bh_r - jet_len), (cx - 35 - spread*2, cy - bh_r - jet_len)
            ], fill=(0, 220, 255, j_alpha))
            draw.polygon([
                (cx - 10 - spread, cy + bh_r - 5), (cx + 10 + spread, cy + bh_r - 5),
                (cx + 35 + spread*2, cy + bh_r + jet_len), (cx - 35 - spread*2, cy + bh_r + jet_len)
            ], fill=(0, 220, 255, j_alpha))

        # 4. Top HUD & Progress Bar
        bar_w = int(W * (frame_idx / total_frames))
        draw.rectangle([0, 0, W, 8], fill=(30, 20, 45, 255))
        draw.rectangle([0, 0, bar_w, 8], fill=(255, 215, 0, 255))

        # Badge
        draw.rounded_rectangle([bx0, by0, bx1, by1], radius=28, fill=(18, 10, 36, 220), outline=(0, 240, 255, 200), width=3)
        draw.text(((W - bw) // 2, 102), badge_text, font=font_badge, fill=(0, 245, 255, 255))

        # 5. Audio Waveform (Reactive to Speech Envelope)
        n_bars = 42
        bar_w_unit = 16
        start_x = (W - n_bars * bar_w_unit) // 2
        for b in range(n_bars):
            h_val = int(8 + 65 * env_val * math.sin(t * 12 + b * 0.4)**2 + 10 * math.cos(b * 0.5)**2)
            bx_b = start_x + b * bar_w_unit
            b_color = (int(255 * (b / n_bars)), int(240 - 25 * (b / n_bars)), int(255 * (1.0 - b / n_bars)), 230)
            draw.line([bx_b, 1180 - h_val, bx_b, 1180 + h_val], fill=b_color, width=5)

        # 6. Dynamic Karaoke Subtitles (Inter Black)
        sub_words = get_current_subtitle(t)
        if sub_words:
            sub_y = 1380
            total_text_w = sum(draw.textlength(w[0] + " ", font=font_sub) for w in sub_words)
            cur_x = (W - total_text_w) // 2

            pad_x = 28
            pad_y = 16
            draw.rounded_rectangle(
                [max(30, cur_x - pad_x), sub_y - pad_y, min(W - 30, cur_x + total_text_w + pad_x), sub_y + 65 + pad_y],
                radius=18, fill=(4, 2, 10, 195), outline=(255, 215, 0, 120), width=2
            )

            for word, is_active in sub_words:
                w_len = draw.textlength(word + " ", font=font_sub)
                if is_active:
                    draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 235, 0, 255),
                              stroke_width=6, stroke_fill=(0, 0, 0, 255))
                else:
                    draw.text((cur_x, sub_y), word, font=font_sub, fill=(255, 255, 255, 220),
                              stroke_width=4, stroke_fill=(0, 0, 0, 255))
                cur_x += w_len

        # 7. Signature (Rule 7: Dasturchi: MuzaffarZed)
        draw.text((wm_x, 1840), wm_text, font=font_wm, fill=(200, 200, 220, 150))

        # Write to FFmpeg
        proc.stdin.write(img.convert("RGB").tobytes())

        if frame_idx % 60 == 0 or frame_idx == total_frames - 1:
            print(f"Rendered {frame_idx}/{total_frames} frames ({t:.2f}s)...")

    proc.stdin.close()
    proc.wait()
    print("DONE! Final video rendered successfully:", output_video)

if __name__ == "__main__":
    main()
