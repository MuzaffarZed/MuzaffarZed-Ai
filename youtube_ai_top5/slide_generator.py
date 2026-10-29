"""
Slide Generator: Yuqori sifatli 1920x1080 Full HD slayd kadrlarini generatsiya qilish moduli.
Zamonaviy dark-mode, neon aksentlar, glassmorphism kartalar, vektor piktogrammalar va toza tipografiya.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REGULAR = "C:/Windows/Fonts/segoeui.ttf"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_checkmark(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color=(255, 255, 255)):
    """Chiroyli va o'tkir vektor checkmark chizish"""
    p1 = (x + int(size * 0.22), y + int(size * 0.50))
    p2 = (x + int(size * 0.44), y + int(size * 0.72))
    p3 = (x + int(size * 0.80), y + int(size * 0.26))
    draw.line([p1, p2, p3], fill=color, width=3, joint="curve")

def draw_play_icon(draw: ImageDraw.ImageDraw, x: int, y: int, w: int = 32, h: int = 22):
    """Qizil YouTube play tugmasi piktogrammasi"""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=(239, 68, 68))
    # Ichidagi oq uchburchak
    tx1, ty1 = x + 12, y + 5
    tx2, ty2 = x + 22, y + 11
    tx3, ty3 = x + 12, y + 17
    draw.polygon([(tx1, ty1), (tx2, ty2), (tx3, ty3)], fill=(255, 255, 255))

def generate_slide(scene: dict, output_path: str, total_scenes: int = 7) -> str:
    width, height = 1920, 1080
    image = Image.new("RGBA", (width, height), (10, 14, 23, 255))
    
    # Ambient Glow yaratish (Neon nur effekti)
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    accent = scene.get("accent_color", (0, 242, 254))
    
    # Orqa fondagi ambient nur doiralari
    glow_draw.ellipse((-120, -120, 500, 500), fill=(accent[0], accent[1], accent[2], 35))
    glow_draw.ellipse((width - 500, height - 500, width + 120, height + 120), fill=(accent[0], accent[1], accent[2], 30))
    glow_draw.ellipse((width // 2 - 200, height // 2 - 200, width // 2 + 200, height // 2 + 200), fill=(accent[0], accent[1], accent[2], 12))
    image = Image.alpha_composite(image, glow_layer)
    
    # Asosiy Card (Glassmorphism container)
    card_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    
    card_x1, card_y1 = 120, 80
    card_x2, card_y2 = 1800, 1000
    
    # Card foni va neon hoshiyasi
    card_bg = (17, 24, 39, 238)
    border_color = scene.get("border_color", (79, 172, 254))
    
    card_draw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=28,
        fill=card_bg,
        outline=border_color,
        width=3
    )
    
    # Top Badge (Pill)
    badge_text = scene.get("badge", "AI SERVISLAR")
    badge_font = get_font(FONT_BOLD, 22)
    badge_bbox = badge_font.getbbox(badge_text)
    badge_w = (badge_bbox[2] - badge_bbox[0]) + 36
    badge_h = 44
    badge_x = card_x1 + 60
    badge_y = card_y1 + 45
    
    card_draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=22,
        fill=(accent[0], accent[1], accent[2], 40),
        outline=(accent[0], accent[1], accent[2], 180),
        width=2
    )
    card_draw.text((badge_x + 18, badge_y + 8), badge_text, font=badge_font, fill=accent)
    
    # Sarlavha (Main Title)
    title_font = get_font(FONT_BOLD, 52)
    title_text = scene.get("title", "")
    card_draw.text((card_x1 + 60, card_y1 + 115), title_text, font=title_font, fill=(255, 255, 255))
    
    # Kichik tavsif (Subtitle)
    subtitle_font = get_font(FONT_REGULAR, 28)
    subtitle_text = scene.get("subtitle", "")
    card_draw.text((card_x1 + 60, card_y1 + 185), subtitle_text, font=subtitle_font, fill=(148, 163, 184))
    
    # Divider line (Chiroyli ajratuvchi chiziq)
    card_draw.line([(card_x1 + 60, card_y1 + 240), (card_x2 - 60, card_y1 + 240)], fill=(45, 55, 72, 180), width=2)
    
    # Chap qism: Bullet points (Asosiy xususiyatlar)
    bullets = scene.get("bullets", [])
    bullet_font = get_font(FONT_BOLD, 28)
    start_y = card_y1 + 295
    spacing = 145
    
    for idx, bullet in enumerate(bullets):
        by = start_y + idx * spacing
        bx = card_x1 + 60
        
        # Glowing Icon doirasi
        circle_d = 46
        card_draw.ellipse(
            [bx, by, bx + circle_d, by + circle_d],
            fill=(accent[0], accent[1], accent[2], 45),
            outline=accent,
            width=2
        )
        
        # Vektor checkmark
        draw_checkmark(card_draw, bx, by, circle_d, color=(255, 255, 255))
        
        # Bullet text (Matnni qatorlarga chiroyli joylash)
        card_draw.text((bx + 68, by + 6), bullet, font=bullet_font, fill=(241, 245, 249))

    # O'ng qism: Highlight Card (Alohida ma'lumotlar va statistik blok)
    highlight = scene.get("highlight")
    if highlight:
        hl_w = 460
        hl_x1 = card_x2 - 60 - hl_w
        hl_y1 = card_y1 + 285
        hl_x2 = card_x2 - 60
        hl_y2 = card_y2 - 120
        
        # Highlight Card foni
        card_draw.rounded_rectangle(
            [hl_x1, hl_y1, hl_x2, hl_y2],
            radius=20,
            fill=(23, 32, 54, 210),
            outline=(accent[0], accent[1], accent[2], 120),
            width=2
        )
        
        # Highlight Header
        hl_tag_font = get_font(FONT_BOLD, 18)
        card_draw.text((hl_x1 + 35, hl_y1 + 30), "VOSITA QISQACHA XARITASI", font=hl_tag_font, fill=accent)
        
        hl_title_font = get_font(FONT_BOLD, 30)
        card_draw.text((hl_x1 + 35, hl_y1 + 60), highlight.get("title", ""), font=hl_title_font, fill=(255, 255, 255))
        
        card_draw.line([(hl_x1 + 35, hl_y1 + 115), (hl_x2 - 35, hl_y1 + 115)], fill=(51, 65, 85), width=2)
        
        # Stat rows
        stats = highlight.get("stats", [])
        stat_y = hl_y1 + 140
        for s_idx, (label, val) in enumerate(stats):
            lbl_font = get_font(FONT_REGULAR, 20)
            val_font = get_font(FONT_BOLD, 26)
            
            card_draw.text((hl_x1 + 35, stat_y), label, font=lbl_font, fill=(148, 163, 184))
            card_draw.text((hl_x1 + 35, stat_y + 28), val, font=val_font, fill=(241, 245, 249))
            
            if s_idx < len(stats) - 1:
                card_draw.line([(hl_x1 + 35, stat_y + 75), (hl_x2 - 35, stat_y + 75)], fill=(38, 48, 70), width=1)
            stat_y += 100
            
    # Footer - Kanal nomi va Progress bar
    footer_y = card_y2 - 60
    
    # YouTube icon va matn
    draw_play_icon(card_draw, card_x1 + 60, footer_y - 2)
    brand_font = get_font(FONT_BOLD, 22)
    card_draw.text((card_x1 + 105, footer_y - 2), "YouTube | AI & Zamonaviy Texnologiyalar", font=brand_font, fill=(148, 163, 184))
    
    # Progress indicator
    scene_id = scene.get("id", 1)
    progress_text = f"Sahna {scene_id} / {total_scenes}"
    prog_font = get_font(FONT_BOLD, 22)
    prog_bbox = prog_font.getbbox(progress_text)
    prog_w = prog_bbox[2] - prog_bbox[0]
    
    prog_x = card_x2 - 60 - prog_w
    card_draw.text((prog_x, footer_y - 2), progress_text, font=prog_font, fill=accent)
    
    # Progress bar line
    bar_w = 220
    bar_x = prog_x - bar_w - 30
    bar_y = footer_y + 6
    card_draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + 8], radius=4, fill=(45, 55, 72))
    
    filled_w = int(bar_w * (scene_id / total_scenes))
    if filled_w > 0:
        card_draw.rounded_rectangle([bar_x, bar_y, bar_x + filled_w, bar_y + 8], radius=4, fill=accent)
        
    final_image = Image.alpha_composite(image, card_layer)
    final_image = final_image.convert("RGB")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_image.save(output_path, quality=95)
    return output_path

def generate_all_slides(scenes: list, output_dir: str) -> list:
    os.makedirs(output_dir, exist_ok=True)
    slide_paths = []
    for scene in scenes:
        filename = f"slide_{scene['id']:02d}.png"
        path = os.path.join(output_dir, filename)
        generate_slide(scene, path, total_scenes=len(scenes))
        slide_paths.append(path)
    return slide_paths

if __name__ == "__main__":
    from content_data import SCENES
    paths = generate_all_slides(SCENES, "output/slides")
    print(f"Barcha {len(paths)} ta yangilangan slayd saqlandi!")
