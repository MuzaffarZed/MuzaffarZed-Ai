"""
Video Assembler: Slaydlar va audio fayllarni birlashtirib, professional Full HD (1080p)
YouTube videosini tayyorlovchi asosiy montaj moduli.
"""

import os
import subprocess

def assemble_scene_video(slide_path: str, audio_path: str, output_path: str) -> str:
    """Bitta sahna uchun rasm va audioni birlashtirib mp4 segment hosil qilish"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", slide_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-ac", "2",
        "-shortest",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Sahna videosini yaratishda ffmpeg xatosi: {result.stderr}")
        
    return output_path

def concatenate_scenes(scene_videos: list, final_output_path: str, temp_dir: str = "output/temp") -> str:
    """Barcha sahna videolarini bitta yakuniy master video fayliga birlashtirish"""
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    concat_list_file = os.path.join(temp_dir, "concat_list.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for vid in scene_videos:
            abs_path = os.path.abspath(vid).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        final_output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Videolarni birlashtirishda ffmpeg xatosi: {result.stderr}")
        
    return final_output_path

def build_full_video(scenes: list, slides_dir: str = "output/slides", audio_dir: str = "output/audio", output_path: str = "output/final_video_top5_ai.mp4") -> str:
    """To'liq montaj tsiklini bajarish"""
    segment_paths = []
    temp_dir = "output/segments"
    os.makedirs(temp_dir, exist_ok=True)
    
    for scene in scenes:
        scene_id = scene["id"]
        slide_file = os.path.join(slides_dir, f"slide_{scene_id:02d}.png")
        audio_file = os.path.join(audio_dir, f"audio_{scene_id:02d}.mp3")
        segment_file = os.path.join(temp_dir, f"segment_{scene_id:02d}.mp4")
        
        if not os.path.exists(slide_file):
            raise FileNotFoundError(f"Slayd topilmadi: {slide_file}")
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio topilmadi: {audio_file}")
            
        print(f"Sahna {scene_id} videosi yig'ilmoqda...")
        assemble_scene_video(slide_file, audio_file, segment_file)
        segment_paths.append(segment_file)
        
    print("Barcha sahnalar birlashtirilmoqda...")
    concatenate_scenes(segment_paths, output_path)
    print(f"Yakuniy video muvaffaqiyatli yaratildi: {output_path}")
    return output_path

if __name__ == "__main__":
    from content_data import SCENES
    build_full_video(SCENES)
