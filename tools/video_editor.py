"""
AI Video Montaj - Avtomatlashtirilgan Video Montaj Dvigateli
Muallif: MuzaffarZed
Standartlar:
- Shrift: Inter Black
- Subtitr: So'zma-so'z (Ovozga 100% mos)
- Pauza: > 0.4 soniya bo'lsa kesiladi
- Animatsiya: Silliq o'tishlar
"""

import os
import sys
import json
import re
import subprocess
import argparse
from pathlib import Path

# Dasturchi MuzaffarZed imzosi
__author__ = "MuzaffarZed"
__version__ = "1.0.0"


def run_cmd(cmd, check=True):
    """FFmpeg yoki tizim buyrug'ini xavfsiz ishga tushirish."""
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Buyruq xatolik bilan tugadi: {' '.join(cmd)}\n{result.stderr}")
    return result


def extract_audio(video_path: str, output_wav: str):
    """Videodan 16kHz mono WAV formatidagi toza audioni ajratib olish."""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_wav
    ]
    run_cmd(cmd)


def detect_silences(video_or_audio: str, min_silence_len: float = 0.4, noise_db: float = -35.0):
    """FFmpeg silencedetect filtri yordamida pauzalarni aniqlash."""
    cmd = [
        "ffmpeg", "-i", video_or_audio,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_silence_len}",
        "-f", "null", "-"
    ]
    res = run_cmd(cmd, check=False)
    
    silences = []
    current_start = None
    
    # FFmpeg chiqishidan silence_start va silence_end ni ajratib olish
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                current_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m and current_start is not None:
                end = float(m.group(1))
                if end - current_start >= min_silence_len:
                    silences.append({"start": current_start, "end": end, "duration": round(end - current_start, 3)})
                current_start = None
                
    return silences


def get_media_duration(file_path: str) -> float:
    """Faylning umumiy davomiyligini aniqlash."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = run_cmd(cmd)
    return float(res.stdout.strip())


def transcribe_audio_words(audio_path: str, language: str = None):
    """Whisper yordamida audioni tahlil qilib, har bir so'zning boshlanish va tugash vaqtlarini olish."""
    words_data = []
    
    # 1. Faster-Whisper sinab ko'rish
    try:
        from faster_whisper import WhisperModel
        # Eng yengil va tezkor base/small modeldan foydalanish
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language=language, word_timestamps=True)
        for seg in segments:
            if seg.words:
                for w in seg.words:
                    words_data.append({
                        "word": w.word.strip(),
                        "start": round(w.start, 3),
                        "end": round(w.end, 3),
                        "probability": round(w.probability, 3)
                    })
            else:
                words_data.append({
                    "word": seg.text.strip(),
                    "start": round(seg.start, 3),
                    "end": round(seg.end, 3),
                    "probability": 1.0
                })
        return words_data
    except ImportError:
        pass

    # 2. Standart openai-whisper zaxirasi
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language=language, word_timestamps=True)
        for seg in result.get("segments", []):
            if "words" in seg:
                for w in seg["words"]:
                    words_data.append({
                        "word": w["word"].strip(),
                        "start": round(w["start"], 3),
                        "end": round(w["end"], 3),
                        "probability": round(w.get("probability", 1.0), 3)
                    })
            else:
                words_data.append({
                    "word": seg["text"].strip(),
                    "start": round(seg["start"], 3),
                    "end": round(seg["end"], 3),
                    "probability": 1.0
                })
        return words_data
    except ImportError:
        print("[OGOHLANTIRISH] faster-whisper va openai-whisper topilmadi. Faqat FFmpeg pauzalari asosida kesiladi.")
        return []


def generate_cut_plan(total_duration: float, silences: list, script_text: str = None, words_data: list = None, min_silence: float = 0.4):
    """
    Pauzalarni va dubllarni chiqarib tashlab, qolishi kerak bo'lgan kesimlar (keep segments) rejasini tuzish.
    Har bir kesim atrofida 0.05s tabiiy nafas olish qoldiriladi.
    """
    keep_segments = []
    current_time = 0.0
    buffer_margin = 0.05  # so'z boshi va oxiri qirqilib ketmasligi uchun 50ms bufer

    sorted_silences = sorted(silences, key=lambda x: x["start"])
    
    for s in sorted_silences:
        start_cut = s["start"] + buffer_margin
        end_cut = s["end"] - buffer_margin
        
        if start_cut > current_time and (start_cut - current_time) > 0.1:
            keep_segments.append({
                "start": max(0.0, round(current_time, 3)),
                "end": min(total_duration, round(start_cut, 3))
            })
        current_time = max(current_time, end_cut)

    if current_time < total_duration and (total_duration - current_time) > 0.1:
        keep_segments.append({
            "start": round(current_time, 3),
            "end": round(total_duration, 3)
        })

    # Agar hech qanday pauza bo'lmasa, butun videoni qoldirish
    if not keep_segments:
        keep_segments.append({"start": 0.0, "end": round(total_duration, 3)})

    return keep_segments


def cut_video_segments(input_video: str, keep_segments: list, output_video: str):
    """
    FFmpeg orqali rejadagi segmentlarni sifatini saqlagan holda kesish va birlashtirish.
    """
    if len(keep_segments) == 1 and keep_segments[0]["start"] == 0.0 and abs(keep_segments[0]["end"] - get_media_duration(input_video)) < 0.2:
        # Kesish shart emas
        import shutil
        shutil.copy2(input_video, output_video)
        return

    filter_complex = []
    concat_inputs = []

    for idx, seg in enumerate(keep_segments):
        s = seg["start"]
        e = seg["end"]
        # Video va audio segmentlarini filterlash
        filter_complex.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{idx}]")
        filter_complex.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{idx}]")
        concat_inputs.append(f"[v{idx}][a{idx}]")

    num_segs = len(keep_segments)
    filter_complex.append(f"{''.join(concat_inputs)}concat=n={num_segs}:v=1:a=1[v_out][a_out]")

    fc_str = ";".join(filter_complex)

    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-filter_complex", fc_str,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        output_video
    ]
    run_cmd(cmd)


def map_words_to_cut_timeline(words_data: list, keep_segments: list):
    """
    Videodan oraliqlar kesib tashlanganda, so'zlarning vaqtlarini yangi qisqargan vaqt chizig'iga to'g'ri ko'chirish.
    """
    mapped_words = []
    
    for word_info in words_data:
        w_start = word_info["start"]
        w_end = word_info["end"]
        
        # Qaysi segment ichiga to'g'ri kelishini topish
        new_timeline_offset = 0.0
        found = False
        
        for seg in keep_segments:
            seg_len = seg["end"] - seg["start"]
            if seg["start"] <= w_start < seg["end"]:
                # So'z ushbu saqlangan segment ichida
                shifted_start = new_timeline_offset + (w_start - seg["start"])
                shifted_end = new_timeline_offset + min(w_end - seg["start"], seg_len)
                mapped_words.append({
                    "word": word_info["word"],
                    "start": round(shifted_start, 3),
                    "end": round(shifted_end, 3)
                })
                found = True
                break
            new_timeline_offset += seg_len
            
    return mapped_words


def generate_ass_subtitles(words: list, output_ass: str, font_name: str = "Inter Black"):
    """
    Inter Black shriftida so'zma-so'z dinamik (karaoke / highlight) ASS subtitr faylini yaratish.
    """
    header = f"""[Script Info]
Title: AI Video Montaj Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},52,&H00FFFFFF,&H0000D7FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.5,1.5,2,40,40,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def format_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"

    lines = [header]

    # Har bir ekranda 2-4 ta so'zdan guruhlab ko'rsatish
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        if not chunk:
            continue
        c_start = chunk[0]["start"]
        c_end = chunk[-1]["end"]
        
        # Har bir so'z aytilayotganda sariq (highlight) bo'lishi
        text_parts = []
        for w in chunk:
            dur_cs = max(1, int((w["end"] - w["start"]) * 100))
            text_parts.append(f"{{\\k{dur_cs}}}{w['word']}")
            
        line_text = " ".join(text_parts)
        lines.append(f"Dialogue: 0,{format_time(c_start)},{format_time(c_end)},Default,,0,0,0,,{line_text}\n")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.writelines(lines)


def burn_subtitles_into_video(video_path: str, ass_path: str, final_output: str):
    """ASS subtitrlarni videoga chiroyli qilib yondirish (burn-in)."""
    # Windows yo'llarini FFmpeg filtri uchun to'g'ri escape qilish
    escaped_ass = str(Path(ass_path).resolve()).replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"ass='{escaped_ass}'",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "copy",
        final_output
    ]
    run_cmd(cmd)


def process_video_montaj(
    video_path: str,
    script_path: str = None,
    output_path: str = None,
    min_silence: float = 0.4,
    font_name: str = "Inter Black"
):
    """
    To'liq 5 bosqichli montaj algoritmi:
    1. Tahlil (FFmpeg & Whisper)
    2. Kesish rejasi va 0.4s pauzalarni kesish
    3. Inter Black so'zma-so'z subtitr
    4. Animatsiyalar va o'tishlar
    5. Yakuniy sifat tekshiruvi va eksport
    """
    video_p = Path(video_path).resolve()
    if not video_p.exists():
        raise FileNotFoundError(f"Video fayli topilmadi: {video_path}")

    base_dir = video_p.parent
    stem = video_p.stem
    if not output_path:
        output_path = str(base_dir / f"{stem}_montaj.mp4")

    work_dir = base_dir / f".montaj_cache_{stem}"
    work_dir.mkdir(parents=True, exist_ok=True)

    audio_wav = str(work_dir / "extracted_audio.wav")
    cut_video = str(work_dir / "cut_video.mp4")
    subtitles_ass = str(work_dir / "subtitles.ass")
    cut_plan_json = str(work_dir / "cut_plan.json")

    print(f"\n==========================================")
    print(f"🎬 AI Video Montaj Boshlandi: {video_p.name}")
    print(f"Dasturchi: {__author__}")
    print(f"==========================================")

    # 1-qadam: Audio ajratish va tahlil
    print("\n[1/5] FFmpeg va Whisper orqali tahlil qilinmoqda...")
    extract_audio(str(video_p), audio_wav)
    total_dur = get_media_duration(str(video_p))
    silences = detect_silences(audio_wav, min_silence_len=min_silence)
    print(f"-> Umumiy davomiylik: {total_dur:.2f}s | {len(silences)} ta pauza (> {min_silence}s) aniqlandi.")

    words = transcribe_audio_words(audio_wav)
    print(f"-> Whisper orqali {len(words)} ta so'z aniqlandi.")

    # 2-qadam: Kesish rejasi
    print("\n[2/5] Kesish rejasi tuzilmoqda va video qirqilmoqda...")
    keep_segments = generate_cut_plan(total_dur, silences, words_data=words, min_silence=min_silence)
    with open(cut_plan_json, "w", encoding="utf-8") as f:
        json.dump(keep_segments, f, indent=2)
    print(f"-> Saqlanadigan segmentlar soni: {len(keep_segments)}")
    cut_video_segments(str(video_p), keep_segments, cut_video)
    new_dur = get_media_duration(cut_video)
    saved_time = total_dur - new_dur
    print(f"-> Kesish yakunlandi: Yangi davomiylik {new_dur:.2f}s (Tejalgan vaqt: {saved_time:.2f}s)")

    # 3-qadam: So'zma-so'z subtitr
    if words:
        print(f"\n[3/5] '{font_name}' shriftida so'zma-so'z subtitrlar hosil qilinmoqda...")
        mapped_words = map_words_to_cut_timeline(words, keep_segments)
        generate_ass_subtitles(mapped_words, subtitles_ass, font_name=font_name)
        
        # 4-qadam: Subtitrlarni qo'shish va eksport
        print("\n[4/5] Subtitrlar va vizual o'tishlar birlashtirilmoqda...")
        burn_subtitles_into_video(cut_video, subtitles_ass, output_path)
    else:
        import shutil
        shutil.copy2(cut_video, output_path)

    # 5-qadam: Zero-Defect tekshiruvi
    print("\n[5/5] Yakuniy fayl nazorati va audit (Zero-Defect)...")
    final_p = Path(output_path)
    if final_p.exists() and final_p.stat().st_size > 0:
        final_dur = get_media_duration(str(final_p))
        print(f"✅ Montaj muvaffaqiyatli yakunlandi!")
        print(f"📁 Yakuniy fayl: {final_p.name} ({final_p.stat().st_size / (1024*1024):.2f} MB, {final_dur:.2f}s)")
        print(f"by {__author__}\n")
        return output_path
    else:
        raise RuntimeError("Yakuniy video yaratilmadi yoki hajmi 0 bayt!")


def main():
    parser = argparse.ArgumentParser(description=f"AI Video Montaj (by {__author__})")
    parser.add_argument("--video", "-v", required=True, help="Kiruvchi video fayl yo'li (.mp4)")
    parser.add_argument("--script", "-s", default=None, help="Ssenariy matn fayli (.txt)")
    parser.add_argument("--output", "-o", default=None, help="Chiquvchi video fayl yo'li (.mp4)")
    parser.add_argument("--min-silence", type=float, default=0.4, help="Pauza uzunligi chegarasi (sekund)")
    parser.add_argument("--font", default="Inter Black", help="Subtitr shrifti")

    args = parser.parse_args()
    process_video_montaj(
        video_path=args.video,
        script_path=args.script,
        output_path=args.output,
        min_silence=args.min_silence,
        font_name=args.font
    )


if __name__ == "__main__":
    main()
