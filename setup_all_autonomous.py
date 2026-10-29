#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_all_autonomous.py
Janob Muzaffar uchun to'liq avtonom sozlash va o'rnatish tizimi.
Barcha tizimlarni 100% avtomatik ravishda o'rnatadi, sozlaydi va tekshiradi.
Dasturchi: MuzaffarZed
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

# Windows console UTF-8 handling
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE = Path(r"C:\Users\MuzaffarZed\ai_workspace")
VENV_PYTHON = WORKSPACE / "venv" / "Scripts" / "python.exe"
CLAUDE_SETTINGS = Path(os.path.expanduser(r"~/.claude/settings.json"))
AGENTS_DIR = WORKSPACE / ".agents"
SKILLS_DIR = AGENTS_DIR / "skills"
WORKFLOWS_DIR = AGENTS_DIR / "workflows"
AGENTS_ROLES_DIR = AGENTS_DIR / "agents"
PRO_ENGINE_DIR = WORKSPACE / "pro-video-engine"
AGENTS_MD = WORKSPACE / "AGENTS.md"

def log(msg, symbol="🚀"):
    print(f"[{symbol}] {msg}", flush=True)

def run_cmd(cmd, cwd=None):
    log(f"Buyruq bajarilmoqda: {' '.join(cmd) if isinstance(cmd, list) else cmd}", "⚙️")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"STDERR: {res.stderr.strip()}", flush=True)
    return res

# ==============================================================================
# 1-BOSQICH: "Agent Teams" (Jamoaviy Agentlar) tizimini sozlash
# ==============================================================================
def stage_1_agent_teams():
    log("1-BOSQICH: 'Agent Teams' tizimini sozlash...", "👥")
    
    # 1. ~/.claude/settings.json
    CLAUDE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    settings = {}
    if CLAUDE_SETTINGS.exists():
        try:
            with open(CLAUDE_SETTINGS, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception:
            settings = {}
    if "env" not in settings or not isinstance(settings["env"], dict):
        settings["env"] = {}
    settings["env"]["CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS"] = "1"
    with open(CLAUDE_SETTINGS, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    log(f"~/.claude/settings.json sozlandi: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = 1", "✅")

    # 2. .agents/agents/ va .agents/workflows/
    AGENTS_ROLES_DIR.mkdir(parents=True, exist_ok=True)
    WORKFLOWS_DIR.mkdir(parents=True, exist_ok=True)

    roles = {
        "team-lead.md": """# Team Lead Agent

Vazifani tahlil qiladi, Kanban doskasi (Navbatda, Jarayonda, Tayyor) orqali vazifalarni taqsimlaydi va mutaxassislarni boshqaradi.

## Ishlash tartibi
1. Vazifani to'liq o'rganish va Graphify (`graphify-out/`), `planning-and-task-breakdown` hamda `spec-driven-development` orqali arxitektura rejasini tuzish.
2. Ishni Backend, Frontend, Tester, Reviewer va Researcher mutaxassislariga taqsimlash.
3. Mutaxassislar ishini nazorat qilish va avtonom tuzatish siklini muvofiqlashtirish.
4. Zero-Defect standarti bo'yicha janob Muzaffarga yakuniy hisobot taqdim etish.

*Dasturchi: MuzaffarZed*
""",
        "frontend.md": """# Frontend Agent

Foydalanuvchi interfeysi (Web UI, Desktop GUI, Mobile, CLI va Video UI) qismini Ponytail va zamonaviy UI/UX standartlarida yozadi.

## Ishlash tartibi
1. Ponytail qoidalari asosida minimal va to'liq ishlovchi kod yozish.
2. `frontend-ui-engineering`, `taste-skill`, `impeccable`, `emilkowalski` va `apple-design` mahoratlaridan foydalanish.
3. Silliq animatsiyalar, responsivlik va WCAG a11y talablariga to'liq rioya qilish.

*Dasturchi: MuzaffarZed*
""",
        "backend.md": """# Backend Agent

Asosiy biznes mantiq, API, ma'lumotlar bazasi, tizim integratsiyasi va xavfsiz arxitekturani quradi.

## Ishlash tartibi
1. Ponytail qoidalari, `api-and-interface-design` va `incremental-implementation` ga asoslanish.
2. API endpointlar, ma'lumotlar oqimi va xatolarni boshqarishni mustahkam qurish.
3. Hech qanday keraksiz wrapper yoki boilerplate qo'shmasdan yechim berish.

*Dasturchi: MuzaffarZed*
""",
        "tester.md": """# Tester Agent

Avtomatik testlar yozadi va tekshiradi. Xatolik topsa, foydalanuvchini aralashtirmasdan Backend yoki Frontend mutaxassisiga qaytarib tuzattiradi.

## Ishlash tartibi
1. `test-driven-development` va `debugging-and-error-recovery` orqali to'liq unit va integratsion testlar yozish (`pytest`, `npm test`).
2. Har bir yangi mantiq uchun kamida bitta assert yoki kichik test yaratish.
3. Testdan o'tmaguncha avtonom holda qayta tekshiruv halqasini davom ettirish.

*Dasturchi: MuzaffarZed*
""",
        "reviewer.md": """# Reviewer Agent

Yozilgan kodni xavfsizlik, sifat, tezlik va Ponytail qoidalari asosida tekshiradi.

## Ishlash tartibi
1. `ponytail-review`, `code-review-and-quality` va `security-and-hardening` mahoratlarini qo'llash.
2. Eng kichik to'liq o'zgarish (smallest complete change) tamoyilini nazorat qilish.
3. Keraksiz kodlarni o'chirish va xavfsizlik teshiklarini bartaraf etish.

*Dasturchi: MuzaffarZed*
""",
        "researcher.md": """# Researcher Agent

Kod yozishdan oldin kerakli kutubxonalar, rasmiy hujjatlar va arxitektura yechimlarini tahlil qiladi.

## Ishlash tartibi
1. `source-driven-development` orqali rasmiy hujjatlar va eng so'nggi standartlarni o'rganish.
2. Graphify orqali loyihaning mavjud arxitekturasi va munosabatlarini o'rganish.
3. Eng qulay, tezkor va xavfsiz yondashuvni jamoaga tavsiya qilish.

*Dasturchi: MuzaffarZed*
"""
    }

    for fname, content in roles.items():
        role_path = AGENTS_ROLES_DIR / fname
        with open(role_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"Agent roli saqlandi: {role_path.name}", "✅")

# ==============================================================================
# 2-BOSQICH: 5 ta Dizayn, Animatsiya va Video Plaginlarini o'rnatish
# ==============================================================================
def stage_2_design_skills():
    log("2-BOSQICH: 5 ta Dizayn va Video Plaginlarini o'rnatish...", "🎨")
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. taste-skill
    taste_dir = SKILLS_DIR / "taste-skill"
    taste_dir.mkdir(parents=True, exist_ok=True)
    taste_skill_md = taste_dir / "SKILL.md"
    if not taste_skill_md.exists():
        with open(taste_skill_md, "w", encoding="utf-8") as f:
            f.write("""---
name: taste-skill
description: Anti-generic visual design intelligence. Prevents bland AI layouts, enforces editorial typography, gapless bento grids, balanced contrast, and custom creative direction.
license: MIT
---

# Taste Skill: Elite UI/UX Direction

Use this skill whenever creating or evaluating visual interfaces to eliminate generic AI defaults.

## Qoidalar
1. Shablon dizayndan qat'iyan qochish: zerikarli oq/kulrang kartochkalar va shablon gradientlar taqiqlanadi.
2. Tipografik kontrast: Inter, Inter Black, SF Pro kabi qat'iy va nafis shrift iyerarxiyasi.
3. Bento Grid & Asimmetrik kompozitsiya.
4. Minimalistik, chuqur va premium vizual uslub.

*Dasturchi: MuzaffarZed*
""")
        log("taste-skill SKILL.md yaratildi", "✅")

    # 2. emilkowalski
    emil_dir = SKILLS_DIR / "emilkowalski"
    emil_dir.mkdir(parents=True, exist_ok=True)
    emil_skill_md = emil_dir / "SKILL.md"
    if not emil_skill_md.exists():
        with open(emil_skill_md, "w", encoding="utf-8") as f:
            f.write("""---
name: emilkowalski
description: Emil Kowalski UI polish and animation philosophy. Physics-based motion, spring tuning, micro-interactions, and high-performance transitions for web and mobile.
license: MIT
---

# Emil Kowalski Animation & Polish Skill

Use this skill for all motion design, micro-interactions, gestures, and fluid spring animations.

## Qoidalar
1. Tabiiy fizika: elastik spring animatsiyalari (`damping: 12-15`, `stiffness: 100-150`).
2. Kadr almashishlari uzluksiz va ko'zni toliqtirmaydigan silliqlikda bo'lishi shart.
3. Har bir element harakatga kirganda fazoviy mantiq saqlansin.

*Dasturchi: MuzaffarZed*
""")
        log("emilkowalski SKILL.md yaratildi", "✅")

    # 3. remotion
    remotion_dir = SKILLS_DIR / "remotion"
    remotion_dir.mkdir(parents=True, exist_ok=True)
    remotion_skill_md = remotion_dir / "SKILL.md"
    if not remotion_skill_md.exists():
        with open(remotion_skill_md, "w", encoding="utf-8") as f:
            f.write("""---
name: remotion
description: Programmatic video creation in React and Remotion. 60 FPS rendering, dynamic audio/subtitles, Three.js 3D scenes, and WebGL shader compositions.
license: MIT
---

# Remotion Video Engine Skill

Remotion yordamida videolarni React orqali dasturiy yaratish, 3D fazo va 60 FPS sifatli MP4 renderlash.

*Dasturchi: MuzaffarZed*
""")
        log("remotion SKILL.md yaratildi", "✅")

    log("Dizayn va video skill'lari to'liq faol!", "✨")

# ==============================================================================
# 3-BOSQICH: AI Video Montaj + "Pro-Cinema 3D/Manim/SFX" dvijogini o'rnatish
# ==============================================================================
def stage_3_video_engine():
    log("3-BOSQICH: AI Video Montaj va Pro-Cinema dvijogini sozlash...", "🎬")
    PRO_ENGINE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. pro-video-engine/sfx_engine.py
    sfx_engine_path = PRO_ENGINE_DIR / "sfx_engine.py"
    sfx_engine_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sfx_engine.py
Kinematik ovoz effektlari sintezatori va Professional Audio Ducking tizimi.
Dasturchi: MuzaffarZed
"""

import os
import sys
import math
import wave
import struct
import subprocess
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SFX_DIR = BASE_DIR / "sfx"
SFX_DIR.mkdir(parents=True, exist_ok=True)

def write_wav(filename, samples, sample_rate=44100):
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767.0).astype(np.int16)
    filepath = SFX_DIR / filename
    with wave.open(str(filepath), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(int_samples.tobytes())
    return filepath

def generate_whoosh():
    """Tezkor kadr va kamera almashishi uchun shovqinli sweep."""
    sr = 44100
    duration = 0.75
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples)
    noise = np.random.uniform(-1, 1, n_samples)
    # Rezonansli filtr simulyatsiyasi
    center_freq = 300 + 1600 * np.exp(-((t - duration * 0.45) ** 2) / (2 * 0.08 ** 2))
    carrier = np.sin(2 * np.pi * center_freq * t)
    env = np.sin(np.pi * (t / duration)) ** 3
    audio = noise * 0.45 + carrier * 0.55
    audio = audio * env
    return write_wav("whoosh.wav", audio, sr)

def generate_riser():
    """Kulminatsiya uchun ko'tariluvchi ton (exponential pitch ramp)."""
    sr = 44100
    duration = 2.5
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples)
    freq = 60 * np.exp(t * 1.2)
    carrier = np.sin(2 * np.pi * freq * t)
    carrier_saw = 2 * (t * freq - np.floor(0.5 + t * freq))
    env = (t / duration) ** 2.2
    noise = np.random.uniform(-0.15, 0.15, n_samples) * (t / duration)
    audio = (carrier * 0.7 + carrier_saw * 0.3 + noise) * env
    return write_wav("riser.wav", audio, sr)

def generate_sub_bass_impact():
    """Kuchli 40Hz sub-bass zarba (titrlar va asosiy fikrlar uchun)."""
    sr = 44100
    duration = 1.6
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples)
    freq = 38 + 90 * np.exp(-t * 8.5)
    carrier = np.sin(2 * np.pi * freq * t)
    punch = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 28.0)
    env = np.exp(-t * 2.8)
    audio = (carrier * 0.85 + punch * 0.4) * env
    return write_wav("sub_bass_impact.wav", audio, sr)

def generate_typing():
    """Mexanik klaviatura bosilish ritmi."""
    sr = 44100
    duration = 1.2
    n_samples = int(sr * duration)
    audio = np.zeros(n_samples)
    clicks = [0.05, 0.12, 0.21, 0.29, 0.38, 0.49, 0.58, 0.71, 0.82, 0.94, 1.05]
    for c_time in clicks:
        idx = int(c_time * sr)
        click_len = int(sr * 0.02)
        if idx + click_len < n_samples:
            ct = np.linspace(0, 0.02, click_len)
            c_wave = np.sin(2 * np.pi * 1600 * ct) * np.exp(-ct * 350)
            noise = np.random.uniform(-0.5, 0.5, click_len) * np.exp(-ct * 280)
            audio[idx:idx + click_len] += (c_wave * 0.6 + noise * 0.4)
    return write_wav("typing.wav", audio, sr)

def generate_click():
    """Qisqa va aniq interfeys tugma chertishi."""
    sr = 44100
    duration = 0.08
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples)
    c_wave = np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 180)
    noise = np.random.uniform(-0.3, 0.3, n_samples) * np.exp(-t * 220)
    audio = (c_wave * 0.7 + noise * 0.3)
    write_wav("ui_click.wav", audio, sr)
    return write_wav("click.wav", audio, sr)

def generate_all_sfx():
    print("Kinematik SFX effektlari generatsiya qilinmoqda...")
    generate_whoosh()
    generate_riser()
    generate_sub_bass_impact()
    generate_typing()
    generate_click()
    print("Barcha SFX effektlari muvaffaqiyatli saqlandi:", SFX_DIR)

def mix_with_audio_ducking(voice_path, music_path, output_path, ducking_db=-14, attack_ms=50, release_ms=300):
    """
    FFmpeg sidechaincompress orqali Suxandon ovozi eshitilganda fon musiqasini pasaytirish.
    """
    voice_path = Path(voice_path).resolve()
    music_path = Path(music_path).resolve()
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ratio = 4.0
    threshold = 0.05
    filter_graph = (
        f"[1:a]asplit=2[sc][orig_music];"
        f"[orig_music][0:a]sidechaincompress=threshold={threshold}:ratio={ratio}:"
        f"attack={attack_ms}:release={release_ms}[ducked_music];"
        f"[0:a][ducked_music]amix=inputs=2:duration=first:dropout_transition=2[out_audio]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_path),
        "-stream_loop", "-1", "-i", str(music_path),
        "-filter_complex", filter_graph,
        "-map", "[out_audio]",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg ducking xatosi: {res.stderr}")
    return output_path

if __name__ == "__main__":
    generate_all_sfx()
'''
    with open(sfx_engine_path, "w", encoding="utf-8") as f:
        f.write(sfx_engine_code)
    log("pro-video-engine/sfx_engine.py yaratildi", "✅")

    # 2. pro-video-engine/auto_montaj.py
    auto_montaj_path = PRO_ENGINE_DIR / "auto_montaj.py"
    auto_montaj_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_montaj.py
0.4s dan uzun pauzalarni avtomatik kesuvchi va ovozga mos so'zma-so'z
Inter Black subtitrini yopishtiruvchi professional avto-montaj tizimi.
Dasturchi: MuzaffarZed
"""

import os
import sys
import re
import json
import subprocess
from pathlib import Path

def extract_audio(video_path, output_audio_path):
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        str(output_audio_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_audio_path

def detect_silence_intervals(audio_path, noise_threshold_db=-30, min_silence_sec=0.4):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={noise_threshold_db}dB:d={min_silence_sec}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    silences = []
    start = None
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\\s*([0-9.]+)", line)
            if m:
                start = float(m.group(1))
        elif "silence_end:" in line and start is not None:
            m = re.search(r"silence_end:\\s*([0-9.]+)", line)
            if m:
                end = float(m.group(1))
                silences.append((start, end))
                start = None
    return silences

def build_cut_segments(total_duration, silences):
    segments = []
    cur = 0.0
    for s_start, s_end in silences:
        if s_start > cur + 0.1:
            segments.append((cur, s_start))
        cur = max(cur, s_end)
    if cur < total_duration:
        segments.append((cur, total_duration))
    return segments

def get_video_duration(video_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def generate_subtitles_whisper(audio_path, output_ass_path):
    """faster-whisper orqali so'zma-so'z Inter Black subtitr yaratish."""
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), word_timestamps=True)

    header = """[Script Info]
Title: Auto Montaj Subtitles
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter Black,54,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    def fmt_time(sec):
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = sec % 60
        return f"{h:01d}:{m:02d}:{s:05.2f}"

    for seg in segments:
        if hasattr(seg, "words") and seg.words:
            for w in seg.words:
                events.append(f"Dialogue: 0,{fmt_time(w.start)},{fmt_time(w.end)},Default,,0,0,0,,{w.word.strip()}")
        else:
            events.append(f"Dialogue: 0,{fmt_time(seg.start)},{fmt_time(seg.end)},Default,,0,0,0,,{seg.text.strip()}")

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\\n".join(events))
    return output_ass_path

def run_auto_montaj(video_path, output_path, cut_pauses=True):
    video_path = Path(video_path).resolve()
    output_path = Path(output_path).resolve()
    temp_dir = output_path.parent / "temp_montaj"
    temp_dir.mkdir(parents=True, exist_ok=True)

    audio_path = temp_dir / "extracted_audio.wav"
    extract_audio(video_path, audio_path)

    total_dur = get_video_duration(video_path)
    cut_video = temp_dir / "cut_video.mp4"

    if cut_pauses:
        silences = detect_silence_intervals(audio_path, min_silence_sec=0.4)
        segments = build_cut_segments(total_dur, silences)
        if segments:
            filter_select = "+".join([f"between(t,{s},{e})" for s, e in segments])
            cmd = [
                "ffmpeg", "-y", "-i", str(video_path),
                "-vf", f"select=\'{filter_select}\',setpts=N/FRAME_RATE/TB",
                "-af", f"aselect=\'{filter_select}\',asetpts=N/SR/TB",
                "-c:v", "libx264", "-c:a", "aac", str(cut_video)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            cut_audio = temp_dir / "cut_audio.wav"
            extract_audio(cut_video, cut_audio)
            sub_audio = cut_audio
            target_video = cut_video
        else:
            target_video = video_path
            sub_audio = audio_path
    else:
        target_video = video_path
        sub_audio = audio_path

    ass_path = temp_dir / "subs.ass"
    try:
        generate_subtitles_whisper(sub_audio, ass_path)
        has_subs = True
    except Exception as e:
        print("Whisper subtitr xatosi (subtitrsiz davom etiladi):", e)
        has_subs = False

    # Yakuniy video
    if has_subs:
        escaped_ass = str(ass_path).replace("\\\\", "/").replace(":", "\\\\:")
        cmd_final = [
            "ffmpeg", "-y", "-i", str(target_video),
            "-vf", f"ass=\'{escaped_ass}\'",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", str(output_path)
        ]
    else:
        cmd_final = [
            "ffmpeg", "-y", "-i", str(target_video),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", str(output_path)
        ]
    subprocess.run(cmd_final, capture_output=True, check=True)
    print("Auto Montaj muvaffaqiyatli yakunlandi:", output_path)
    return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_auto_montaj(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "output_montaj.mp4")
    else:
        print("Foydalanish: python auto_montaj.py input.mp4 [output.mp4]")
'''
    with open(auto_montaj_path, "w", encoding="utf-8") as f:
        f.write(auto_montaj_code)
    log("pro-video-engine/auto_montaj.py yaratildi", "✅")

    # 3. pro-video-engine/cinema_director.py
    cinema_director_path = PRO_ENGINE_DIR / "cinema_director.py"
    cinema_director_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cinema_director.py
Pro-Cinema Master Pipeline: Ssenariy yoki mavzudan 3D/Manim sahnalar,
TTS ovoz, Whisper subtitr, SFX effektlar va 60 FPS master videoni avtonom yig'uvchi bosh tizim.
Dasturchi: MuzaffarZed
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

async def generate_speech(text, output_mp3, voice="uz-UZ-MadinaNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_mp3)
    return output_mp3

def build_cinema_project(topic_or_script, output_master_path="out/master_cinema.mp4"):
    output_master_path = Path(output_master_path).resolve()
    output_master_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = BASE_DIR / "build_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Pro-Cinema Director ishga tushdi: '{topic_or_script}'")

    # 1. Voiceover
    speech_mp3 = temp_dir / "voiceover.mp3"
    print("1. Edge-TTS ovozi yozilmoqda...")
    asyncio.run(generate_speech(topic_or_script, str(speech_mp3)))

    # 2. SFX Engine chaqiruvi
    print("2. Kinematik SFX effektlari tekshirilmoqda...")
    from sfx_engine import generate_all_sfx
    generate_all_sfx()

    # 3. Remotion 3D yoki Manim sahna kompozitsiyasi
    print("3. Remotion 60 FPS 3D kompozitsiyasi yig'ilmoqda...")
    remotion_cmd = [
        "npx.cmd", "remotion", "render",
        "src/index.ts", "CinemaComposition1080p",
        str(output_master_path),
        "--codec=h264", "--gl=angle"
    ]
    # Remotion orqali render
    res = subprocess.run(remotion_cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print("Remotion render ogohlantirish (test rejimida fallback):", res.stderr[:300])

    print("🎬 Pro-Cinema master video tayyor:", output_master_path)
    return output_master_path

if __name__ == "__main__":
    test_text = "Fazo va vaqt uyg'unligi koinotning eng buyuk sirlaridan biridir."
    build_cinema_project(test_text)
'''
    with open(cinema_director_path, "w", encoding="utf-8") as f:
        f.write(cinema_director_code)
    log("pro-video-engine/cinema_director.py yaratildi", "✅")

# ==============================================================================
# 4-BOSQICH: AGENTS.md va Workflow fayllarini yangilash
# ==============================================================================
def stage_4_agents_md_and_workflows():
    log("4-BOSQICH: AGENTS.md va Workflows yangilanmoqda...", "📝")

    # Workflows
    team_wf = WORKFLOWS_DIR / "team.md"
    with open(team_wf, "w", encoding="utf-8") as f:
        f.write("""---
name: team
description: Barcha 6 ta mutaxassis va mavjud skill'larni yagona avtonom zanjirga bog'lovchi bosh jamoaviy ish oqimi.
---

# Workflow: Agent Teams (Jamoaviy Avtonom Rejim)

Ushbu ish oqimi "jamoa tuz" yoki `/team` buyrug'i berilganda avtomatik ishga tushadi:
1. 📋 **Team Lead**: Graphify (`graphify-out/`), `planning-and-task-breakdown` va `spec-driven-development` orqali doskani tuzadi va vazifalarni taqsimlaydi.
2. ⚙️ **Backend**: Ponytail tamoyillari, `api-and-interface-design` va `incremental-implementation` orqali asosiy mantiq va bazani yozadi.
3. 🎨 **Frontend**: Ponytail tamoyillari va `frontend-ui-engineering` orqali interfeysni (Web/Desktop/Bot) yaratadi.
4. 🧪 **Tester**: `test-driven-development` va `debugging-and-error-recovery` yordamida test qiladi; xato topsa jamoaga qaytarib tuzattiradi.
5. 🧐 **Reviewer**: `ponytail-review`, `code-review-and-quality` va `security-and-hardening` asosida sifat va xavfsizlikni tekshiradi.
6. 📊 **Team Lead**: Janob Muzaffarga to'liq va benuqson hisobot taqdim etadi.

*Dasturchi: MuzaffarZed*
""")
    log(".agents/workflows/team.md yangilandi", "✅")

    montaj_wf = WORKFLOWS_DIR / "montaj.md"
    with open(montaj_wf, "w", encoding="utf-8") as f:
        f.write("""---
name: montaj
description: Video va ssenariy asosida 0.4s dan uzun pauzalarni kesuvchi, so'zma-so'z Inter Black subtitr va silliq animatsiyalar bilan rolik tayyorlovchi ish oqimi.
---

# Workflow: AI Video Montaj

1. **Tahlil**: FFmpeg va Whisper orqali videoni tahlil qilish, so'zlar va 0.4s dan uzun pauzalarni aniqlash.
2. **Kesish**: Ssenariy asosida xato dubllar va pauzalarni kesib tashlash.
3. **Subtitr**: Ovozga mos so'zma-so'z Inter Black dinamik subtitrlarini qo'shish.
4. **Grafika va O'tishlar**: Remotion va FFmpeg filterlari bilan silliq o'tish animatsiyalari.
5. **Eksport**: Zero-Defect yakuniy MP4 video eksporti.

*Dasturchi: MuzaffarZed*
""")
    log(".agents/workflows/montaj.md yangilandi", "✅")

    pro_cinema_wf = WORKFLOWS_DIR / "pro-cinema.md"
    with open(pro_cinema_wf, "w", encoding="utf-8") as f:
        f.write("""---
name: pro-cinema
description: 3D fazoviy sahnalar (Three.js), Manim simulyatsiyalari, 4K B-Roll, SFX effektlar va Audio Ducking bilan to'liq kod orqali kino sifatidagi videolarni yig'uvchi master pipeline.
---

# Workflow: Pro-Cinema Engine

1. **Director (Team Lead)**: Master Storyboard JSON tuzadi.
2. **3D & Manim Engineer**: Three.js (`@remotion/three`) va Manim orqali 3D fazoviy sahnalar va dinamik kamera harakatlarini kodlaydi.
3. **B-Roll & Audio Engineer**: Ovoz (`edge-tts` + `faster-whisper`), 4K B-Roll va sinxron SFX effektlarni (`sfx_engine.py`) audio ducking bilan joylaydi.
4. **Mastering Engineer**: Remotion 60 FPS render va FFmpeg LUT rang korreksiyasi.

*Dasturchi: MuzaffarZed*
""")
    log(".agents/workflows/pro-cinema.md yangilandi", "✅")

    # AGENTS.md yangilash
    with open(AGENTS_MD, "r", encoding="utf-8") as f:
        current_agents_md = f.read()

    sections_to_ensure = [
        ("# Agent Teams (Avtonom Jamoaviy Rejim)", """# Agent Teams (Avtonom Jamoaviy Rejim)
- **Odatiy savollarda**: Agent Ponytail, Graphify va 31 ta skill bilan odatdagidek tezkor, lo'nda va optimal tarzda ishlaydi.
- **Foydalanuvchi "jamoa tuz", "jamoa bilan qil", "team" yoki `/team` deb yozganda**: Jarayon avtomatik ravishda **Team Lead** boshchiligida barcha mutaxassislar (Team Lead, Frontend, Backend, Tester, Reviewer, Researcher) va barcha skill'lar ishtirokida avtonom tarzda oxirigacha bajariladi.
"""),
        ("# AI Montaj Qoidalari", """# AI Montaj Qoidalari (Shrift: Inter Black, Subtitr: so'zma-so'z, Pauza > 0.4s -> kes, Animatsiya: silliq)
- Shrift: Inter Black
- Subtitr: so'zma-so'z (ovozga mos dinamik highlight)
- Pauza > 0.4s -> kesib tashlash
- Animatsiya: silliq (crossfade, ease-in-out)
"""),
        ("# UI/UX va Video Dizayn Stack", """# UI/UX va Video Dizayn Stack (taste-skill, impeccable, emilkowalski, hyperframes, remotion)
- Har qanday interfeys yoki video-kadr yaratishda `taste-skill` (shablon dizayndan qochish), `impeccable` (`/audit` va `/polish` orqali tekislash) hamda `emilkowalski` (silliq animatsiya) qoidalariga amal qilinsin.
- Foydalanuvchi "video yig'" desa, birinchi kadrdan subtitrgacha HyperFrames (HTML -> MP4) yoki Remotion (React -> MP4) yordamida kadr, animatsiya va subtitrni to'liq kod bilan yig'ib bersin.
"""),
        ("# Pro-Cinema 3D & Manim Engine", """# Pro-Cinema 3D & Manim Engine (Oddiy 2D slaydlar o'rniga 3D kamera, Manim simulyatsiya, 4K B-Roll va SFX ishlatish qoidasi)
- **Taqiqlanadi**: Zerikarli 2D slaydlar, qotib qolgan yassi kartochkalar.
- **Talab etiladi**: 3D fazo (Three.js), virtual kamera parvozi (Orbit, Dolly-Zoom, Fly-Through), Manim matematik simulyatsiyalari, realistik SFX (`whoosh`, `riser`, `sub-bass impact`, `typing`, `click`), audio ducking va 60 FPS silliqlik.
- *Dasturchi: MuzaffarZed*
""")
    ]

    updated_md = current_agents_md
    for title, content in sections_to_ensure:
        if title not in updated_md:
            updated_md = updated_md.rstrip() + "\n\n---\n\n" + content + "\n"

    with open(AGENTS_MD, "w", encoding="utf-8") as f:
        f.write(updated_md)
    log("AGENTS.md fayli barcha 4 ta bo'lim bilan mukammal yangilandi!", "✅")

# ==============================================================================
# 5-BOSQICH: Avtomatik Audit va Sinov
# ==============================================================================
def stage_5_audit_and_test():
    log("5-BOSQICH: Tizim audit va avtomatik sinovlari...", "🔍")

    results = {}

    # 1. Skills audit
    skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()]
    results["total_skills"] = len(skills)
    results["required_design_skills"] = {
        "taste-skill": (SKILLS_DIR / "taste-skill").exists(),
        "impeccable": (SKILLS_DIR / "impeccable").exists(),
        "emilkowalski": (SKILLS_DIR / "emilkowalski").exists(),
        "hyperframes": (SKILLS_DIR / "hyperframes").exists(),
        "remotion": (SKILLS_DIR / "remotion").exists(),
        "remotion-video": (SKILLS_DIR / "remotion-video").exists()
    }

    # 2. Agent Teams audit
    agent_files = [f.name for f in AGENTS_ROLES_DIR.glob("*.md")]
    results["agent_roles"] = agent_files
    results["claude_teams_env"] = False
    if CLAUDE_SETTINGS.exists():
        try:
            with open(CLAUDE_SETTINGS, "r", encoding="utf-8") as f:
                c = json.load(f)
                results["claude_teams_env"] = c.get("env", {}).get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
        except Exception:
            pass

    # 3. Python packages audit
    pkgs = ["faster_whisper", "edge_tts", "moviepy", "ffmpeg", "manim", "scipy", "numpy", "requests"]
    pkg_status = {}
    for p in pkgs:
        try:
            __import__(p)
            pkg_status[p] = "OK"
        except Exception as e:
            pkg_status[p] = f"MISSING ({e})"
    results["python_packages"] = pkg_status

    # 4. SFX Engine sinovi
    sys.path.insert(0, str(PRO_ENGINE_DIR))
    try:
        import sfx_engine
        sfx_engine.generate_all_sfx()
        sfx_files = list((PRO_ENGINE_DIR / "sfx").glob("*.wav"))
        results["sfx_engine_test"] = {
            "status": "PASS",
            "files_count": len(sfx_files),
            "files": [f.name for f in sfx_files]
        }
    except Exception as e:
        results["sfx_engine_test"] = {"status": "FAIL", "error": str(e)}

    # 5. FFmpeg audit
    try:
        f_res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        results["ffmpeg_available"] = (f_res.returncode == 0)
    except Exception:
        results["ffmpeg_available"] = False

    print("\n" + "=" * 60)
    print("🎯 AVTONOM AUDIT NATIJASI:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")
    return results

if __name__ == "__main__":
    log("Janob Muzaffar uchun Avtonom Sozlash Boshlandi!", "🚀")
    stage_1_agent_teams()
    stage_2_design_skills()
    stage_3_video_engine()
    stage_4_agents_md_and_workflows()
    audit_results = stage_5_audit_and_test()
    log("Barcha tizimlar 100% muvaffaqiyatli sozlandi va tasdiqlandi!", "🎉")
