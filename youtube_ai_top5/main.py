"""
Master Pipeline: YouTube uchun to'liq video va barcha resurslarni bir bosishda yaratish.
1. Slaydlar (1920x1080)
2. Tabiiy AI ovozlar (Edge-TTS Sardor Neural)
3. Full HD master video (1080p MP4)
4. Yuqori CTR muqovasi (Thumbnail)
"""

import sys
import time
from content_data import SCENES
from slide_generator import generate_all_slides
from audio_generator import generate_all_audios
from video_assembler import build_full_video
from thumbnail_generator import generate_thumbnail

def run_pipeline():
    start_time = time.time()
    print("=" * 65)
    print("🚀 YOUTUBE AVTOMATIK VIDEO GENERATORI ISHGA TUSHMOQDA...")
    print("=" * 65)
    
    # 1. Slaydlar
    print("\n[1/4] 🎨 1080p Slaydlar generatsiya qilinmoqda...")
    slides = generate_all_slides(SCENES, "output/slides")
    print(f"✓ {len(slides)} ta Full HD slayd muvaffaqiyatli tayyorlandi.")
    
    # 2. Audio
    print("\n[2/4] 🎙️ O'zbekcha AI ovozlar sintez qilinmoqda...")
    audios = generate_all_audios(SCENES, "output/audio")
    total_audio_sec = sum(a["duration"] for a in audios)
    print(f"✓ {len(audios)} ta audio tayyorlandi. Jami davomiylik: {total_audio_sec:.1f} soniya.")
    
    # 3. Montaj va Video
    print("\n[3/4] 🎬 Full HD master video yig'ilmoqda...")
    video_path = build_full_video(SCENES, "output/slides", "output/audio", "output/final_video_top5_ai.mp4")
    print(f"✓ Yakuniy video tayyor: {video_path}")
    
    # 4. Thumbnail
    print("\n[4/4] 🖼️ YouTube Thumbnail yaratilmoqda...")
    thumb_path = generate_thumbnail("output/thumbnail.png")
    print(f"✓ Muqova tayyorlandi: {thumb_path}")
    
    elapsed = time.time() - start_time
    print("\n" + "=" * 65)
    print(f"🎉 BARCHA BOSQICHLAR MUVAFFAQIYATLI YAKUNLANDI! ({elapsed:.1f} soniya)")
    print("Barcha fayllar 'output/' papkasida jamlandi:")
    print(" - Video: output/final_video_top5_ai.mp4")
    print(" - Muqova: output/thumbnail.png")
    print(" - Ssenariy & SEO: youtube_seo.md")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline()
