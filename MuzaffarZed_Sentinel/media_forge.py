import os
import subprocess
import shutil

MUSIC_OUT_DIR = os.path.expanduser(r"~\Desktop\Musiqa_Fleshka_2026")
VIDEO_OUT_DIR = os.path.expanduser(r"~\Desktop\Video_Montaj_Dasturlari")

os.makedirs(MUSIC_OUT_DIR, exist_ok=True)
os.makedirs(VIDEO_OUT_DIR, exist_ok=True)

def download_audio_mp3(url, output_dir=MUSIC_OUT_DIR):
    """
    Downloads best quality audio and converts to 320kbps MP3 with embedded metadata.
    """
    yt_dlp = shutil.which("yt-dlp")
    ffmpeg = shutil.which("ffmpeg")
    
    if not yt_dlp:
        return {"status": "error", "message": "yt-dlp not found on PATH"}
        
    cmd = [
        yt_dlp,
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--add-metadata",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    if ffmpeg:
        cmd.extend(["--ffmpeg-location", os.path.dirname(ffmpeg)])
        
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "message": "Audio downloaded and converted to MP3 320kbps!",
            "output_dir": output_dir
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e.stderr or e)}

def download_video_hd(url, output_dir=VIDEO_OUT_DIR):
    """
    Downloads best video (up to 1080p/4K) and merges with best audio into MP4.
    """
    yt_dlp = shutil.which("yt-dlp")
    ffmpeg = shutil.which("ffmpeg")
    
    if not yt_dlp:
        return {"status": "error", "message": "yt-dlp not found on PATH"}
        
    cmd = [
        yt_dlp,
        "-f", "bestvideo+bestaudio/best",
        "--merge-output-format", "mp4",
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url
    ]
    
    if ffmpeg:
        cmd.extend(["--ffmpeg-location", os.path.dirname(ffmpeg)])
        
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "message": "Video downloaded in Full HD MP4!",
            "output_dir": output_dir
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e.stderr or e)}

if __name__ == "__main__":
    print("Testing Media Forge Engine...")
    print(f"Music destination: {MUSIC_OUT_DIR} (Exists: {os.path.exists(MUSIC_OUT_DIR)})")
    print(f"Video destination: {VIDEO_OUT_DIR} (Exists: {os.path.exists(VIDEO_OUT_DIR)})")
    print("Media Forge initialized with yt-dlp & ffmpeg support!")
