"""
Audio Generator: O'zbek tilidagi tabiiy AI ovoz (Sardor Neural) yordamida har bir sahna
uchun kristaldek toza ovozli audio fayllarni yaratish moduli.
"""

import os
import subprocess
import shutil

VOICE = "uz-UZ-SardorNeural"

def generate_scene_audio(text: str, output_path: str, rate: str = "+0%") -> str:
    """Bitta sahna uchun audio faylni edge-tts orqali yaratish"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "edge-tts",
        "--text", text,
        "--voice", VOICE,
        "--rate", rate,
        "--write-media", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Audio yaratishda xatolik yuz berdi: {result.stderr}")
    
    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        raise RuntimeError(f"Yaratilgan audio fayl bo'sh yoki mavjud emas: {output_path}")
        
    return output_path

def get_audio_duration(audio_path: str) -> float:
    """ffprobe yordamida audio faylning aniq davomiyligini (sekundda) olish"""
    cmd = [
        "ffprobe",
        "-i", audio_path,
        "-show_entries", "format=duration",
        "-v", "quiet",
        "-of", "csv=p=0"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe xatosi: {result.stderr}")
    return float(result.stdout.strip())

def generate_all_audios(scenes: list, output_dir: str) -> list:
    """Barcha sahnalar uchun audiolarni generatsiya qilish va davomiyligini qaytarish"""
    os.makedirs(output_dir, exist_ok=True)
    results = []
    
    for scene in scenes:
        scene_id = scene["id"]
        filename = f"audio_{scene_id:02d}.mp3"
        path = os.path.join(output_dir, filename)
        
        script_text = scene.get("script", "")
        generate_scene_audio(script_text, path)
        duration = get_audio_duration(path)
        
        results.append({
            "id": scene_id,
            "audio_path": path,
            "duration": duration
        })
        print(f"Sahna {scene_id} audiosi tayyorlandi: {duration:.2f} soniya ({filename})")
        
    return results

if __name__ == "__main__":
    from content_data import SCENES
    audios = generate_all_audios(SCENES, "output/audio")
    total_duration = sum(a["duration"] for a in audios)
    print(f"Umumiy video davomiyligi: {total_duration:.2f} soniya ({total_duration/60:.1f} daqiqa)")
