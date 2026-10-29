import os
import sys
import subprocess
from pathlib import Path

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine")
WORKSPACE = Path(r"C:\Users\MuzaffarZed\ai_workspace")
TEMP = ENGINE_DIR / "temp_comedy_v2"

RAW_VIDEO = TEMP / "comedy_raw_v2.mp4"
MASTER_AUDIO = TEMP / "master_audio.wav"
ASS_SUBS = TEMP / "subtitles.ass"

OUTPUT_MAIN = WORKSPACE / "kulguli_dasturchi_video.mp4"
OUTPUT_LONG = WORKSPACE / "kulguli_dasturchi_video_uzun.mp4"

def main():
    print("🎬 Yakuniy uzun komediya videosini yig'ish (Burn-in Inter Black Subtitles)...")
    if not RAW_VIDEO.exists():
        print("XATO: Raw video topilmadi:", RAW_VIDEO)
        sys.exit(1)
    if not MASTER_AUDIO.exists():
        print("XATO: Master audio topilmadi:", MASTER_AUDIO)
        sys.exit(1)
    if not ASS_SUBS.exists():
        print("XATO: Subtitr fayli topilmadi:", ASS_SUBS)
        sys.exit(1)

    escaped_ass = str(ASS_SUBS).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", str(RAW_VIDEO),
        "-i", str(MASTER_AUDIO),
        "-vf", f"ass='{escaped_ass}'",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "256k",
        "-shortest",
        str(OUTPUT_MAIN)
    ]
    print("Running FFmpeg assembly...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr)
        sys.exit(1)

    # Also copy or link to OUTPUT_LONG
    import shutil
    shutil.copyfile(str(OUTPUT_MAIN), str(OUTPUT_LONG))

    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(OUTPUT_MAIN)]
    dur = float(subprocess.check_output(dur_cmd, text=True).strip())
    size_mb = os.path.getsize(OUTPUT_MAIN) / (1024 * 1024)

    print(f"🎉 MUVAFFAQIYAT! Video tayyor: {OUTPUT_MAIN}")
    print(f"⏱️ Davomiyligi: {dur:.2f} soniya ({dur/60:.2f} daqiqa / 1 daqiqa {int(dur%60)} soniya)!")
    print(f"📊 Hajmi: {size_mb:.2f} MB")

if __name__ == "__main__":
    main()
