import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

OVERLAY_DIR = r"C:\Users\MuzaffarZed\ai_workspace\creator_overlays"
os.makedirs(OVERLAY_DIR, exist_ok=True)
FRAMES_DIR = os.path.join(OVERLAY_DIR, "temp_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

WIDTH, HEIGHT = 1080, 1080
FPS = 30
CHROMA_GREEN = (0, 255, 0)

# Try to find a bold font
FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = r"C:\Users\MuzaffarZed\ai_workspace\creator_fonts\Montserrat-Bold.ttf"

def clear_frames():
    for f in os.listdir(FRAMES_DIR):
        if f.endswith('.png'):
            os.remove(os.path.join(FRAMES_DIR, f))

def encode_mp4(out_filename, num_frames):
    out_path = os.path.join(OVERLAY_DIR, out_filename)
    frame_pattern = os.path.join(FRAMES_DIR, "frame_%04d.png")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", frame_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Rendered: {out_filename}")
    clear_frames()

# ==========================================
# 1. SUBSCRIBE & BELL BUTTON
# ==========================================
def render_subscribe():
    print("Rendering 01_Subscribe_Bell_Button.mp4...")
    clear_frames()
    total_frames = 120 # 4s
    font_large = ImageFont.truetype(FONT_PATH, 56)
    font_small = ImageFont.truetype(FONT_PATH, 48)

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS # time in seconds

        # Button center at (540, 540)
        btn_w, btn_h = 560, 130
        x0 = (WIDTH - btn_w) // 2
        y0 = (HEIGHT - btn_h) // 2
        x1 = x0 + btn_w
        y1 = y0 + btn_h

        is_subscribed = t >= 1.6
        bg_color = (80, 80, 80) if is_subscribed else (235, 32, 38)
        text = "SUBSCRIBED" if is_subscribed else "SUBSCRIBE"

        # Pop effect on click at 1.5s
        scale = 1.0
        if 1.4 <= t < 1.6:
            scale = 0.94
        elif 1.6 <= t < 1.8:
            scale = 1.05

        cur_w = int(btn_w * scale)
        cur_h = int(btn_h * scale)
        cx0 = (WIDTH - cur_w) // 2
        cy0 = (HEIGHT - cur_h) // 2
        cx1 = cx0 + cur_w
        cy1 = cy0 + cur_h

        # Rounded button
        draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=35, fill=bg_color, outline=(255, 255, 255), width=4)

        # Draw Bell icon on right
        bell_x = cx1 - 90
        bell_y = cy0 + cur_h // 2
        bell_shake = math.sin(t * 35) * 6 if (1.6 <= t <= 2.8) else 0
        draw.ellipse([bell_x - 22 + bell_shake, bell_y - 25, bell_x + 22 + bell_shake, bell_y + 15], fill=(255, 215, 0))
        draw.polygon([(bell_x - 30 + bell_shake, bell_y + 15), (bell_x + 30 + bell_shake, bell_y + 15), (bell_x + bell_shake, bell_y - 28)], fill=(255, 215, 0))
        draw.ellipse([bell_x - 8 + bell_shake, bell_y + 14, bell_x + 8 + bell_shake, bell_y + 26], fill=(255, 215, 0))

        # Text
        cur_font = font_small if is_subscribed else font_large
        draw.text((cx0 + 45, cy0 + (cur_h - 60)//2), text, fill=(255, 255, 255), font=cur_font)

        # Click pointer hand
        if 0.8 <= t < 1.7:
            # moving towards button
            hand_progress = min(1.0, (t - 0.8) / 0.6)
            hand_x = int(650 - (1.0 - hand_progress) * 150)
            hand_y = int(580 + (1.0 - hand_progress) * 200)
            if t >= 1.4:
                hand_y += 8
            # draw pointer cursor
            draw.polygon([(hand_x, hand_y), (hand_x, hand_y + 50), (hand_x + 15, hand_y + 38), (hand_x + 32, hand_y + 58), (hand_x + 42, hand_y + 52), (hand_x + 25, hand_y + 32), (hand_x + 42, hand_y + 32)], fill=(255, 255, 255), outline=(0, 0, 0), width=3)

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("01_Subscribe_Bell_Button.mp4", total_frames)

# ==========================================
# 2. LIKE THUMBS UP POP
# ==========================================
def render_like():
    print("Rendering 02_Like_ThumbsUp_Pop.mp4...")
    clear_frames()
    total_frames = 90 # 3s
    font = ImageFont.truetype(FONT_PATH, 52)

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        # Elastic scale in 0 to 0.5s
        if t < 0.5:
            progress = t / 0.5
            scale = math.sin(progress * math.pi * 0.7) * 1.2
        else:
            scale = 1.0 + 0.05 * math.sin((t - 0.5) * 5)

        r = int(180 * scale)
        cx, cy = WIDTH // 2, HEIGHT // 2 - 40

        # Circle blue badge
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 119, 242), outline=(255, 255, 255), width=int(8 * scale))

        # Thumbs up graphic inside
        tr = int(80 * scale)
        # Thumb
        draw.rounded_rectangle([cx - tr//3, cy - tr, cx + tr//4, cy + tr//2], radius=int(15*scale), fill=(255, 255, 255))
        # Fist
        draw.rounded_rectangle([cx - tr, cy - tr//4, cx + tr//2, cy + tr], radius=int(20*scale), fill=(255, 255, 255))

        # "LIKE" text underneath
        if t > 0.3:
            draw.text((cx - 65, cy + r + 30), "LIKE!", fill=(255, 255, 255), font=font, stroke_width=4, stroke_fill=(0, 0, 0))

        # Sparkles / stars around
        if t > 0.35:
            for angle_deg in [30, 80, 140, 200, 260, 320]:
                rad = math.radians(angle_deg)
                sparkle_dist = r + 60 + int(30 * math.sin((t * 8) + angle_deg))
                sx = cx + int(sparkle_dist * math.cos(rad))
                sy = cy + int(sparkle_dist * math.sin(rad))
                draw.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(255, 230, 0))

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("02_Like_ThumbsUp_Pop.mp4", total_frames)

# ==========================================
# 3. RED ARROW POINTER
# ==========================================
def render_arrow():
    print("Rendering 03_Red_Arrow_Pointer.mp4...")
    clear_frames()
    total_frames = 90

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        # Bouncing offset
        bounce = int(45 * math.sin(t * 7))
        base_x = WIDTH // 2 + bounce
        base_y = HEIGHT // 2

        # Draw sharp stylish neon red arrow pointing left
        # Arrow shaft
        draw.rectangle([base_x, base_y - 35, base_x + 220, base_y + 35], fill=(255, 20, 40), outline=(255, 255, 255), width=6)
        # Arrow head
        points = [
            (base_x, base_y - 95),
            (base_x - 130, base_y),
            (base_x, base_y + 95)
        ]
        draw.polygon(points, fill=(255, 20, 40), outline=(255, 255, 255))
        # Inner gloss
        draw.line([(base_x - 110, base_y), (base_x + 190, base_y)], fill=(255, 180, 180), width=8)

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("03_Red_Arrow_Pointer.mp4", total_frames)

# ==========================================
# 4. COUNTDOWN 5s
# ==========================================
def render_countdown():
    print("Rendering 04_Countdown_5s.mp4...")
    clear_frames()
    total_frames = 150 # 5s
    font = ImageFont.truetype(FONT_PATH, 160)

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        sec = 5 - int(t)
        if sec < 1:
            sec = 1
        sub_t = t % 1.0

        # Circle pulse
        r = 220 + int(20 * (1.0 - sub_t))
        cx, cy = WIDTH // 2, HEIGHT // 2

        # Outer glowing ring
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 20, 20), outline=(255, 255, 255), width=10)
        # Progress arc
        start_angle = -90
        end_angle = -90 + int(360 * sub_t)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start_angle, end=end_angle, fill=(255, 60, 60), width=14)

        # Number text
        text = str(sec)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((cx - tw//2, cy - th//2 - 20), text, fill=(255, 255, 255), font=font)

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("04_Countdown_5s.mp4", total_frames)

# ==========================================
# 5. QUESTION MARKS CONFUSED
# ==========================================
def render_questions():
    print("Rendering 05_Question_Marks.mp4...")
    clear_frames()
    total_frames = 90
    font = ImageFont.truetype(FONT_PATH, 130)

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        # 3 question marks with different offsets and wobble
        marks = [
            (WIDTH//2 - 180, HEIGHT//2 - int(40 * math.sin(t*4)), 0.9, -15),
            (WIDTH//2,       HEIGHT//2 - 60 - int(50 * math.cos(t*5)), 1.2, 10),
            (WIDTH//2 + 180, HEIGHT//2 - int(35 * math.sin(t*4.5 + 1)), 0.85, -8),
        ]

        for qx, qy, scale, rot in marks:
            draw.text((qx - 40, qy - 70), "?", fill=(255, 235, 0), font=font, stroke_width=8, stroke_fill=(30, 30, 30))

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("05_Question_Marks.mp4", total_frames)

# ==========================================
# 6. MONEY CASH RAIN
# ==========================================
def render_money():
    print("Rendering 06_Money_Cash_Rain.mp4...")
    clear_frames()
    total_frames = 90
    font = ImageFont.truetype(FONT_PATH, 38)

    # 15 falling bills
    bills = []
    for k in range(16):
        bills.append({
            'x': (k * 70 + 40) % (WIDTH - 150),
            'speed': 280 + (k * 25) % 200,
            'y_offset': (k * 130) % 900,
            'w': 160,
            'h': 85
        })

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        for b in bills:
            cur_y = int(b['y_offset'] + t * b['speed']) % (HEIGHT + 200) - 100
            cur_x = b['x'] + int(30 * math.sin(t * 3 + b['x']))

            # Banknote
            draw.rounded_rectangle([cur_x, cur_y, cur_x + b['w'], cur_y + b['h']], radius=10, fill=(133, 187, 101), outline=(46, 125, 50), width=4)
            draw.ellipse([cur_x + b['w']//2 - 25, cur_y + b['h']//2 - 25, cur_x + b['w']//2 + 25, cur_y + b['h']//2 + 25], outline=(46, 125, 50), width=3)
            draw.text((cur_x + b['w']//2 - 12, cur_y + b['h']//2 - 22), "$", fill=(46, 125, 50), font=font)

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("06_Money_Cash_Rain.mp4", total_frames)

# ==========================================
# 7. FIRE ENERGY FLAME
# ==========================================
def render_fire():
    print("Rendering 07_Fire_Energy_Flame.mp4...")
    clear_frames()
    total_frames = 90

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        # Multi-layered stylized fire flames at bottom
        for flame_idx in range(12):
            fx = 80 + flame_idx * 85
            flame_h = 240 + int(90 * math.sin(t * 12 + flame_idx * 1.5))

            # Outer Red flame
            draw.polygon([
                (fx - 55, HEIGHT),
                (fx, HEIGHT - flame_h),
                (fx + 55, HEIGHT)
            ], fill=(235, 45, 20))

            # Middle Orange flame
            draw.polygon([
                (fx - 35, HEIGHT),
                (fx + int(10*math.sin(t*15)), HEIGHT - int(flame_h * 0.75)),
                (fx + 35, HEIGHT)
            ], fill=(255, 140, 0))

            # Inner Yellow core
            draw.polygon([
                (fx - 20, HEIGHT),
                (fx, HEIGHT - int(flame_h * 0.45)),
                (fx + 20, HEIGHT)
            ], fill=(255, 235, 50))

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("07_Fire_Energy_Flame.mp4", total_frames)

# ==========================================
# 8. HEART LOVE REACTIONS
# ==========================================
def render_hearts():
    print("Rendering 08_Heart_Love_Reactions.mp4...")
    clear_frames()
    total_frames = 90

    hearts = []
    for k in range(12):
        hearts.append({
            'x': (k * 90 + 60) % (WIDTH - 120),
            'speed': 240 + (k * 30) % 180,
            'y_offset': (k * 150) % 900,
            'size': 40 + (k * 10) % 35
        })

    for i in range(total_frames):
        img = Image.new("RGB", (WIDTH, HEIGHT), CHROMA_GREEN)
        draw = ImageDraw.Draw(img)
        t = i / FPS

        for h in hearts:
            cur_y = HEIGHT - (int(h['y_offset'] + t * h['speed']) % (HEIGHT + 200))
            cur_x = h['x'] + int(35 * math.sin(t * 3.5 + h['x']))
            s = h['size']

            # Draw heart using two circles and a triangle
            draw.ellipse([cur_x - s, cur_y - s, cur_x, cur_y], fill=(255, 20, 80))
            draw.ellipse([cur_x, cur_y - s, cur_x + s, cur_y], fill=(255, 20, 80))
            draw.polygon([(cur_x - s, cur_y - s//3), (cur_x + s, cur_y - s//3), (cur_x, cur_y + int(s * 1.1))], fill=(255, 20, 80))

        img.save(os.path.join(FRAMES_DIR, f"frame_{i:04d}.png"))

    encode_mp4("08_Heart_Love_Reactions.mp4", total_frames)

if __name__ == "__main__":
    render_subscribe()
    render_like()
    render_arrow()
    render_countdown()
    render_questions()
    render_money()
    render_fire()
    render_hearts()
    print("All 8 Creator Green Screen Overlays successfully generated!")
