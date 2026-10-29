import asyncio
import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import edge_tts

TEMP = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine\temp_comedy_v2")
TEMP.mkdir(parents=True, exist_ok=True)
ENGINE_DIR = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine")
SFX_DIR = ENGINE_DIR / "sfx"

# 6 epizod ssenariysi
SCENES = [
    {
        "id": "scene1",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+6%",
        "pitch": "+1Hz",
        "text": "Kechki soat sakkiz. Hamma uyda, choy ichib dam olyapti. Dasturchi esa: Bo'ldi, bugun faqat bitta Saqlash tugmasining rangini ko'k qilib qo'yaman-u, besh minutda uxlayman, dedi. Ishoning, eng katta xatolar aynan mana shu gapdan keyin boshlanadi!"
    },
    {
        "id": "scene2",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+10%",
        "pitch": "+2Hz",
        "text": "Oradan ikki yarim soat o'tdi. Tugma ko'k bo'ldi, ammo nega butun baza o'chib ketdi?! Foydalanuvchilarning hisobidagi balans minus bir milliard! Boshlandi haqiqiy fojia!"
    },
    {
        "id": "scene3",
        "voice": "uz-UZ-MadinaNeural",
        "rate": "+6%",
        "pitch": "+2Hz",
        "text": "Tungi soat birda mijoz qo'ng'iroq qilyapti: Salom, uxlab yotganmidingiz? Nega saytga kirsam qop-qora ekran bo'lib, Siz koinotdagi eng baxtli xakersiz deb yozib qo'yibdi?! Ertalab investorlar oldida taqdimotim bor, tezda to'g'irlang!"
    },
    {
        "id": "scene4",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+8%",
        "pitch": "+1Hz",
        "text": "Dasturchi esa: Havotir olmang, bu yangi kreativ marketing funksiyasi, hozir to'g'irlaymiz, dedi. StackOverflow esa shunchaki kompyuterni derazadan uloqtiring debdi! AI esa tasalli berib she'r to'qimoqda! Rahmat senga, juda yordam berding!"
    },
    {
        "id": "scene5",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+10%",
        "pitch": "+2Hz",
        "text": "Tungi soat besh. O'n sakkizinchi chashka kofe. Ventilyator reaktiv samolyotdek uvillamoqda! Oxirgi chora: git push origin main force! Nima bo'lsa bo'ldi!"
    },
    {
        "id": "scene6",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+6%",
        "pitch": "+1Hz",
        "text": "Va nihoyat ertalab ma'lum bo'ldi: butun muammo bitta ortiqcha nuqta-vergulda ekan! Uni o'chirgandik, sayt mo'jizadek ishlab ketdi! Dasturchi bo'lish oson, asablar esa qayta tiklanmaydi!"
    }
]

async def generate_speech():
    print("🎙️ Ovozlar generatsiya qilinmoqda...")
    for item in SCENES:
        out_f = TEMP / f"{item['id']}.mp3"
        print(f"  -> {item['id']}: {item['voice']}...")
        comm = edge_tts.Communicate(item["text"], item["voice"], rate=item["rate"], pitch=item["pitch"])
        await comm.save(str(out_f))
    print("✅ Barcha ovoz fayllari tayyor!")

def get_duration(file_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)

def generate_comedy_music(total_duration, sample_rate=44100):
    print(f"🎵 {total_duration:.1f} soniyalik dinamik fon musiqasi sintezlanmoqda...")
    out_wav = TEMP / "bgm.wav"
    t = np.linspace(0, total_duration, int(sample_rate * total_duration))
    
    # 124 BPM Upbeat Funk/Comedy groove
    tempo = 124
    beat_dur = 60.0 / tempo
    beats = int(total_duration / beat_dur)

    music = np.zeros_like(t)

    # Chord progression: Am7 -> D9 -> Fmaj7 -> E7alt
    roots = [220.00, 146.83, 174.61, 164.81]

    for b in range(beats):
        b_start = b * beat_dur
        idx_start = int(b_start * sample_rate)
        idx_end = int(min(total_duration, b_start + beat_dur * 0.9) * sample_rate)
        sub_t = t[idx_start:idx_end] - b_start
        
        chord_root = roots[(b // 4) % len(roots)]
        # Slap-style funky bass
        bass = np.sin(2 * np.pi * chord_root * sub_t) * np.exp(-sub_t * 5.0)
        # Funky staccato synth stab
        synth = np.sin(2 * np.pi * (chord_root * 2) * sub_t) * 0.25 * np.exp(-sub_t * 9.0)
        
        music[idx_start:idx_end] += (bass * 0.45 + synth)

    # Hi-hat & shaker groove
    for b in range(beats * 4):
        b_start = b * (beat_dur / 4)
        idx_start = int(b_start * sample_rate)
        idx_end = int(min(total_duration, b_start + 0.04) * sample_rate)
        sub_t = t[idx_start:idx_end] - b_start
        hat = np.random.uniform(-0.12, 0.12, len(sub_t)) * np.exp(-sub_t * 45.0)
        music[idx_start:idx_end] += hat

    # Outro fade
    fade_len = int(sample_rate * 2.5)
    music[-fade_len:] *= np.linspace(1, 0, fade_len)

    final_music = np.clip(music * 0.4, -1.0, 1.0)
    int_music = (final_music * 32767).astype(np.int16)

    with wave.open(str(out_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_music.tobytes())
    return out_wav

def main():
    asyncio.run(generate_speech())
    
    # Analyze timings
    timings = {}
    total_voice_dur = 0
    pause_between = 0.6  # 0.6s pause between scenes
    current_time = 0.0

    scene_starts = []
    for item in SCENES:
        f = TEMP / f"{item['id']}.mp3"
        dur = get_duration(f)
        scene_starts.append({
            "id": item["id"],
            "start": current_time,
            "duration": dur,
            "end": current_time + dur,
            "file": str(f)
        })
        print(f"Epizod {item['id']}: start={current_time:.2f}s, dur={dur:.2f}s, end={current_time+dur:.2f}s")
        current_time += dur + pause_between

    total_duration = current_time + 1.5 # 1.5s outro
    print(f"\n🎬 JAMI VIDEO DAVOMIYLIGI: {total_duration:.1f} soniya ({total_duration/60:.2f} daqiqa)!")

    # BGM
    bgm_wav = generate_comedy_music(total_duration)

    # Build FFmpeg filter complex for speech concatenation & SFX
    # 0 = scene1, 1 = scene2, 2 = scene3, 3 = scene4, 4 = scene5, 5 = scene6
    # 6 = bgm
    # 7.. = sfx
    sfx_whoosh = SFX_DIR / "whoosh.wav"
    sfx_subbass = SFX_DIR / "sub_bass_impact.wav"
    sfx_click = SFX_DIR / "ui_click.wav"
    sfx_typing = SFX_DIR / "typing.wav"
    sfx_riser = SFX_DIR / "riser.wav"

    # Save timings to JSON for Remotion & Whisper
    import json
    with open(TEMP / "timings.json", "w", encoding="utf-8") as jf:
        json.dump({"total_duration": total_duration, "scenes": scene_starts}, jf, indent=2)

    # Concat speech into one track with exact delays
    speech_filters = []
    for i, sc in enumerate(scene_starts):
        ms = int(sc["start"] * 1000)
        speech_filters.append(f"[{i}:a]adelay={ms}|{ms}[sc_{i}];")
    
    amix_inputs = "".join([f"[sc_{i}]" for i in range(len(scene_starts))])
    speech_mix = f"{amix_inputs}amix=inputs={len(scene_starts)}:duration=longest:dropout_transition=0[all_speech]"

    # Combine speech + ducked music + SFX
    # SFX events:
    # 0s: Sub-bass (Intro impact)
    # scene2 start: riser + sub-bass
    # scene3 start: whoosh + double click (phone ring)
    # scene4 start: whoosh + typing
    # scene5 start: riser + sub-bass
    # scene6 start: whoosh + sub-bass
    sfx_inputs = [
        str(sfx_subbass), # idx 7
        str(sfx_riser),   # idx 8
        str(sfx_whoosh),  # idx 9
        str(sfx_typing),  # idx 10
        str(sfx_click),   # idx 11
    ]

    sfx_cmds = []
    # 0s sub-bass
    sfx_cmds.append("[7:a]adelay=0|0,volume=1.0[sfx0];")
    # scene 2 start (disaster)
    s2_ms = int(scene_starts[1]["start"] * 1000)
    sfx_cmds.append(f"[8:a]adelay={max(0, s2_ms-1000)}|{max(0, s2_ms-1000)},volume=0.8[sfx1];")
    sfx_cmds.append(f"[7:a]adelay={s2_ms}|{s2_ms},volume=1.1[sfx2];")
    # scene 3 start (phone ring / whoosh)
    s3_ms = int(scene_starts[2]["start"] * 1000)
    sfx_cmds.append(f"[9:a]adelay={s3_ms}|{s3_ms},volume=0.9[sfx3];")
    sfx_cmds.append(f"[11:a]adelay={s3_ms+400}|{s3_ms+400},volume=1.2[sfx4];")
    # scene 4 start
    s4_ms = int(scene_starts[3]["start"] * 1000)
    sfx_cmds.append(f"[9:a]adelay={s4_ms}|{s4_ms},volume=0.9[sfx5];")
    sfx_cmds.append(f"[10:a]adelay={s4_ms+500}|{s4_ms+500},volume=0.9[sfx6];")
    # scene 5 start
    s5_ms = int(scene_starts[4]["start"] * 1000)
    sfx_cmds.append(f"[8:a]adelay={max(0, s5_ms-1000)}|{max(0, s5_ms-1000)},volume=0.8[sfx7];")
    sfx_cmds.append(f"[7:a]adelay={s5_ms}|{s5_ms},volume=1.1[sfx8];")
    # scene 6 start
    s6_ms = int(scene_starts[5]["start"] * 1000)
    sfx_cmds.append(f"[9:a]adelay={s6_ms}|{s6_ms},volume=0.9[sfx9];")
    sfx_cmds.append(f"[7:a]adelay={s6_ms+1000}|{s6_ms+1000},volume=1.0[sfx10];")

    all_sfx_mix = "".join([f"[sfx{k}]" for k in range(11)]) + "amix=inputs=11:duration=longest:dropout_transition=0[all_sfx];"

    # Ducking: duck music when speech is present
    ducking = (
        "[6:a][all_speech]sidechaincompress=threshold=0.03:ratio=4:attack=50:release=350[ducked_bgm];"
        "[ducked_bgm][all_sfx]amix=inputs=2:duration=longest:dropout_transition=0[bgm_and_sfx];"
        "[all_speech][bgm_and_sfx]amix=inputs=2:duration=first:dropout_transition=0[master_final]"
    )

    full_filter = "".join(speech_filters) + speech_mix + ";" + "".join(sfx_cmds) + all_sfx_mix + ducking

    master_wav = TEMP / "master_audio.wav"
    ffmpeg_cmd = ["ffmpeg", "-y"]
    for sc in scene_starts:
        ffmpeg_cmd.extend(["-i", sc["file"]])
    ffmpeg_cmd.extend(["-i", str(bgm_wav)])
    for sfx_p in sfx_inputs:
        ffmpeg_cmd.extend(["-i", sfx_p])

    ffmpeg_cmd.extend([
        "-filter_complex", full_filter,
        "-map", "[master_final]",
        "-t", f"{total_duration:.2f}",
        "-c:a", "pcm_s16le",
        str(master_wav)
    ])

    print("🎚️ FFmpeg master audio mikslash...")
    res = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr)
        raise RuntimeError("FFmpeg master audio failed")
    print("✅ Master audio 100% tayyor:", master_wav)

if __name__ == "__main__":
    main()
