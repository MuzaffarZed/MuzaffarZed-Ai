"""
Thumbnail Generator: YouTube uchun bosish darajasi (CTR) o'ta yuqori bo'lgan
1280x720 o'lchamdagi professional muqova (thumbnail) yaratish moduli.
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

def draw_lightning_bolt(draw: ImageDraw.ImageDraw, x: int, y: int, color=(251, 191, 36)):
    """Chiroyli sariq chaqmoq (lightning) belgisi"""
    points = [
        (x + 10, y),
        (x + 2, y + 14),
        (x + 8, y + 14),
        (x + 4, y + 26),
        (x + 16, y + 10),
        (x + 10, y + 10)
    ]
    draw.polygon(points, fill=color)

def generate_thumbnail(output_path: str = "output/thumbnail.png") -> str:
    w, h = 1280, 720
    img = Image.new("RGBA", (w, h), (10, 14, 26, 255))
    
    # Gradient va Ambient yorug'lik
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Neon nur dog'lari
    glow_draw.ellipse((-100, -100, 500, 500), fill=(0, 242, 254, 60))      # Cyan nur
    glow_draw.ellipse((w - 550, -100, w + 100, 500), fill=(168, 85, 247, 55)) # Purple nur
    glow_draw.ellipse((w // 2 - 200, h - 300, w // 2 + 400, h + 200), fill=(245, 158, 11, 45)) # Amber nur
    img = Image.alpha_composite(img, glow)
    
    draw = ImageDraw.Draw(img)
    
    # Markaziy kartochka ramkasi (Cyberpunk glass card)
    card_margin_x, card_margin_y = 50, 40
    card_w, card_h = w - card_margin_x * 2, h - card_margin_y * 2
    
    # Semi-transparent fon
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rounded_rectangle(
        [card_margin_x, card_margin_y, card_margin_x + card_w, card_margin_y + card_h],
        radius=24,
        fill=(17, 24, 39, 215),
        outline=(0, 242, 254, 180),
        width=3
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # 1. Yuqori qizil badge: [ 2026-YIL TRENDLARI ]
    badge_x, badge_y = 85, 75
    badge_w, badge_h = 300, 48
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=24,
        fill=(220, 38, 38),
        outline=(239, 68, 68),
        width=2
    )
    badge_font = get_font(FONT_BOLD, 22)
    draw.text((badge_x + 25, badge_y + 9), "2026-YIL TRENDLARI", font=badge_font, fill=(255, 255, 255))
    
    # Bepul statusi: [ 100% BEPUL ]
    status_x = badge_x + badge_w + 20
    draw.rounded_rectangle(
        [status_x, badge_y, status_x + 190, badge_y + badge_h],
        radius=24,
        fill=(16, 185, 129),
        outline=(52, 211, 153),
        width=2
    )
    draw.text((status_x + 24, badge_y + 9), "100% BEPUL", font=badge_font, fill=(255, 255, 255))
    
    # 2. Asosiy katta sarlavhalar (Ultra CTR matnlar)
    t1_font = get_font(FONT_BOLD, 64)
    t2_font = get_font(FONT_BOLD, 68)
    t3_font = get_font(FONT_BOLD, 68)
    
    def draw_text_with_shadow(pos, text, font, fill, shadow_color=(0, 0, 0, 220), offset=(4, 4)):
        draw.text((pos[0] + offset[0], pos[1] + offset[1]), text, font=font, fill=shadow_color)
        draw.text(pos, text, font=font, fill=fill)
        
    start_ty = 160
    draw_text_with_shadow((85, start_ty), "HAYOTINGIZNI 10X", t1_font, (250, 204, 21))     # Bright Yellow
    draw_text_with_shadow((85, start_ty + 82), "TEZLASHTIRUVCHI", t2_font, (255, 255, 255))   # White
    draw_text_with_shadow((85, start_ty + 172), "TOP 5 TA AI VOSITA!", t3_font, (0, 242, 254)) # Cyan
    
    # 3. O'ng tomondagi ko'rgazmali texnologiya nishonlari (Badges container)
    p_x1, p_y1 = 780, 145
    p_x2, p_y2 = 1195, 530
    
    draw.rounded_rectangle([p_x1, p_y1, p_x2, p_y2], radius=18, fill=(24, 32, 54, 230), outline=(168, 85, 247), width=2)
    
    tag_font = get_font(FONT_BOLD, 20)
    draw.text((p_x1 + 25, p_y1 + 25), "TOP RO'YXAT:", font=tag_font, fill=(168, 85, 247))
    
    tools = [
        ("01", "Perplexity AI", (45, 212, 191)),
        ("02", "v0.dev", (168, 85, 247)),
        ("03", "Gamma App", (236, 72, 153)),
        ("04", "ElevenLabs", (99, 102, 241)),
        ("05", "NotebookLM", (34, 197, 94))
    ]
    
    item_y = p_y1 + 72
    for num, name, color in tools:
        draw.rounded_rectangle([p_x1 + 25, item_y, p_x1 + 65, item_y + 36], radius=8, fill=color)
        num_font = get_font(FONT_BOLD, 18)
        draw.text((p_x1 + 33, item_y + 6), num, font=num_font, fill=(255, 255, 255))
        
        name_font = get_font(FONT_BOLD, 22)
        draw.text((p_x1 + 80, item_y + 6), name, font=name_font, fill=(241, 245, 249))
        item_y += 62
        
    # 4. Pastki qism: Chaqiriq va branding
    footer_y = h - card_margin_y - 75
    draw.line([(85, footer_y - 15), (w - 85, footer_y - 15)], fill=(51, 65, 85), width=2)
    
    draw_lightning_bolt(draw, 85, footer_y)
    call_font = get_font(FONT_BOLD, 24)
    draw.text((115, footer_y), "HAR BIR INSON BILISHI SHART BO'LGAN SERVISLAR", font=call_font, fill=(251, 191, 36))
    
    final_img = img.convert("RGB")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_img.save(output_path, quality=95)
    return output_path

if __name__ == "__main__":
    out = generate_thumbnail("output/thumbnail.png")
    print(f"Mukammal Thumbnail saqlandi: {out}")
