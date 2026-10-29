import asyncio
import json
import os
import sys
import wave
import subprocess
import numpy as np
from pathlib import Path
import edge_tts

# Force UTF-8 on Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine")
TEMP = ENGINE_DIR / "temp_acting_v3"
TEMP.mkdir(parents=True, exist_ok=True)
SFX_DIR = ENGINE_DIR / "sfx"

# 16 ta jonli, ifodali, dramatik dialog replikalari
DRAMA_CUES = [
    # --- 1-SAHNA: SOAT 20:00 (Tinchlik va soxta ishonch) ---
    {
        "id": "c01_intro",
        "scene": 1,
        "role": "narrator",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-3%",
        "pitch": "-1Hz",
        "pause_after": 0.4,
        "text": "Kechki soat sakkiz... Oshxona tinch, hamma maza qilib issiq choy ichyapti."
    },
    {
        "id": "c02_dev_confident",
        "scene": 1,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+6%",
        "pitch": "+2Hz",
        "pause_after": 0.45,
        "text": "Bizning dasturchi esa monitorga qarab: Bo'ldi! Hozir bitta Saqlash tugmasini ko'k qilib qo'yaman-u, besh minutda uxlayman! dedi."
    },
    {
        "id": "c03_fojia_ogoh",
        "scene": 1,
        "role": "narrator",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-6%",
        "pitch": "-2Hz",
        "pause_after": 0.6,
        "text": "Eh birodar... Eng katta kutilmagan fojialar aynan mana shu gapdan boshlanishini u hali bilmas edi..."
    },

    # --- 2-SAHNA: SOAT 22:30 (Qizil xavf va shok) ---
    {
        "id": "c04_shock",
        "scene": 2,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+12%",
        "pitch": "+4Hz",
        "pause_after": 0.35,
        "text": "Oradan ikki soat o'tdi... To'xta! Bu nima?! Tugma ko'k bo'ldi-yu... LEKIN BAZA QANI?!"
    },
    {
        "id": "c05_panic",
        "scene": 2,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+15%",
        "pitch": "+5Hz",
        "pause_after": 0.7,
        "text": "Voy dod! Barcha foydalanuvchilarning hisobidagi balans... minus bir milliard bo'lib ketibdi-ku! Server esa yonyapti! Qani mening ma'lumotlarim?!"
    },

    # --- 3-SAHNA: TUNGI 01:15 (Injiq mijozning telefon qo'ng'irog'i) ---
    {
        "id": "c06_boss_call",
        "scene": 3,
        "role": "boss_phone", # Telefon filtri qo'yiladi!
        "voice": "uz-UZ-MadinaNeural",
        "rate": "+8%",
        "pitch": "+3Hz",
        "pause_after": 0.45,
        "text": "Allo?! Muzaffar! Uxlab yotganmidingiz?! Nega saytga kirsam qop-qora ekran bo'lib, Siz koinotdagi eng baxtli xakersiz deb yozib qo'yibdi?! Ertalab investorlar oldida taqdimotim bor, tezda to'g'irlang!"
    },
    {
        "id": "c07_dev_excuse",
        "scene": 3,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-1%",
        "pitch": "+1Hz",
        "pause_after": 0.65,
        "text": "Assalomu alaykum, hurmatli mijoz... Havotir olmang! Bu xato emas... Bu bizning yangi, zamonaviy kreativ marketing funksiyamiz! Hozir ozgina sozlayapmiz..."
    },

    # --- 4-SAHNA: SOAT 03:00 (StackOverflow va AI) ---
    {
        "id": "c08_stackoverflow_search",
        "scene": 4,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-4%",
        "pitch": "-1Hz",
        "pause_after": 0.35,
        "text": "Soat tungi uch... Ko'zlar qizargan. StackOverflow'ga kiraman."
    },
    {
        "id": "c09_stackoverflow_answer",
        "scene": 4,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+7%",
        "pitch": "+1Hz",
        "pause_after": 0.4,
        "text": "Mutaxassis yozibdi: Sizning muammoingiz hal bo'lmaydi. Shunchaki kompyuterni derazadan uloqtiring! Ha, rahmat, juda yordam berding!"
    },
    {
        "id": "c10_ai_ask",
        "scene": 4,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+5%",
        "pitch": "+2Hz",
        "pause_after": 0.3,
        "text": "Endi sun'iy intellektdan so'raymiz: AIjon, meni qutqar!"
    },
    {
        "id": "c11_ai_reply",
        "scene": 4,
        "role": "ai_robot",
        "voice": "uz-UZ-MadinaNeural",
        "rate": "-6%",
        "pitch": "-2Hz",
        "pause_after": 0.35,
        "text": "Kechirasiz, men til modeliman, ammo sizga tasalli beruvchi g'amgin ruboiy to'qib berishim mumkin..."
    },
    {
        "id": "c12_ai_thanks",
        "scene": 4,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-2%",
        "pitch": "-1Hz",
        "pause_after": 0.65,
        "text": "Voy xudo... Yordaming uchun katta rahmat!"
    },

    # --- 5-SAHNA: SOAT 05:30 (Ventilyator uvillashi va Git Push Force) ---
    {
        "id": "c13_fan_sound",
        "scene": 5,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+12%",
        "pitch": "+3Hz",
        "pause_after": 0.35,
        "text": "Tungi soat besh! O'n sakkizinchi chashka kofe! Kompyuter ventilyatori reaktiv samolyotdek uvillamoqda!"
    },
    {
        "id": "c14_git_push",
        "scene": 5,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+18%",
        "pitch": "+6Hz",
        "pause_after": 0.75,
        "text": "Oxirgi chora: Git push origin main force! Nima bo'lsa bo'ldi! Samolyot parvozga tayyor!"
    },

    # --- 6-SAHNA: SOAT 08:00 (Buyuk nuqta-vergul mo'jizasi va xulosa) ---
    {
        "id": "c15_semicolon_found",
        "scene": 6,
        "role": "narrator",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-2%",
        "pitch": "-1Hz",
        "pause_after": 0.45,
        "text": "Va nihoyat... Ertalab soat sakkizda bilsak..."
    },
    {
        "id": "c16_victory",
        "scene": 6,
        "role": "dev",
        "voice": "uz-UZ-SardorNeural",
        "rate": "+6%",
        "pitch": "+2Hz",
        "pause_after": 0.5,
        "text": "To'qqiz soat qidirilgan buyuk fojia... koddagi bitta ortiqcha nuqta-vergulda ekan! Uni o'chirgandik — butun sayt mo'jizadek ishlab ketdi!"
    },
    {
        "id": "c17_conclusion",
        "scene": 6,
        "role": "narrator",
        "voice": "uz-UZ-SardorNeural",
        "rate": "-1%",
        "pitch": "-1Hz",
        "pause_after": 1.2,
        "text": "Xulosa shuki: Dasturchi bo'lish juda oson... Ammo asablar esa qayta tiklanmaydi! Dasturchi: MuzaffarZed!"
    }
]

async def generate_raw_cues():
    print("🎙️ 17 ta dramatik jonli aktyorlik replikalari sintezlanmoqda...")
    for cue in DRAMA_CUES:
        raw_mp3 = TEMP / f"{cue['id']}_raw.mp3"
        comm = edge_tts.Communicate(cue["text"], cue["voice"], rate=cue["rate"], pitch=cue["pitch"])
        await comm.save(str(raw_mp3))
        print(f"  -> {cue['id']}: {cue['role']} ({cue['voice']})")
    print("✅ Barcha replikalar tayyorlandi!")

def load_audio_ffmpeg(path, sr=44100):
    cmd = [
        "ffmpeg", "-y", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le",
        "-ar", str(sr), "-ac", "1", "-"
    ]
    raw = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0

def apply_vocal_fx(input_mp3, output_wav, role):
    """
    Har bir qahramon ovoziga mos studiya akustikasi:
    - boss_phone: Haqiqiy telefon trubkasi filtri (bandpass 400Hz - 3400Hz)
    - ai_robot: Toza neyron / biroz robotik fazoviy effekt
    - dev / narrator: Shure SM7B podkast studiya harorati (Boy bass + tiniq yuqori chastota)
    """
    if role == "boss_phone":
        # Haqiqiy kiruvchi telefon qo'ng'irog'i filtri
        af = "highpass=f=400,lowpass=f=3400,volume=1.35,equalizer=f=1800:width_type=h:width=500:g=3"
    elif role == "ai_robot":
        af = "equalizer=f=300:width_type=h:width=100:g=-3,equalizer=f=4000:width_type=h:width=1000:g=4,volume=1.1"
    else:
        # Boy podkast ovozi: iliq ko'krak rezonansi (140Hz) va tiniq diktor artikulyatsiyasi (3.5kHz)
        af = "equalizer=f=140:width_type=h:width=80:g=2.8,equalizer=f=3500:width_type=h:width=1200:g=3.2,volume=1.15"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_mp3),
        "-af", af,
        "-ar", "44100", "-ac", "1",
        str(output_wav)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_upbeat_comedy_music(total_duration, sample_rate=44100):
    print(f"🎵 {total_duration:.1f} soniyalik ritmik komediya BGM musiqasi sintezlanmoqda...")
    out_wav = TEMP / "bgm_funk.wav"
    t = np.linspace(0, total_duration, int(sample_rate * total_duration))
    
    # 124 BPM Upbeat Funk/Comedy groove
    tempo = 124
    beat_dur = 60.0 / tempo
    beats = int(total_duration / beat_dur)

    music = np.zeros_like(t)

    # Akkordlar ketma-ketligi (Am7 -> D9 -> Fmaj7 -> E7)
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

    final_music = np.clip(music * 0.38, -1.0, 1.0)
    int_music = (final_music * 32767).astype(np.int16)

    with wave.open(str(out_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_music.tobytes())
    return out_wav

def main():
    asyncio.run(generate_raw_cues())

    sr = 44100
    processed_cues = []
    current_time = 0.0

    print("🎚️ Har bir replikaga studiya ovozi va telefon filtrlari berilmoqda...")
    for cue in DRAMA_CUES:
        raw_mp3 = TEMP / f"{cue['id']}_raw.mp3"
        processed_wav = TEMP / f"{cue['id']}_proc.wav"
        apply_vocal_fx(raw_mp3, processed_wav, cue["role"])

        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(processed_wav)]
        dur = float(subprocess.check_output(dur_cmd, text=True).strip())

        processed_cues.append({
            **cue,
            "file": str(processed_wav),
            "start": current_time,
            "duration": dur,
            "end": current_time + dur
        })
        current_time += dur + cue["pause_after"]

    total_duration = current_time + 1.5 # 1.5s outro
    total_samples = int(total_duration * sr)
    print(f"\n🎬 JAMI ANIMATSIYA DAVOMIYLIGI: {total_duration:.2f} soniya ({total_duration/60:.2f} daqiqa)!")

    # BGM musiqasi
    bgm_wav = generate_upbeat_comedy_music(total_duration, sample_rate=sr)

    # Timing ma'lumotlarini JSON ga saqlash (Remotion va Whisper uchun)
    # Sahna boshlanish vaqtlarini aniqlash
    scene_start_times = {}
    for c in processed_cues:
        sc_num = c["scene"]
        if sc_num not in scene_start_times:
            scene_start_times[sc_num] = c["start"]

    timings_data = {
        "total_duration": total_duration,
        "scene_starts": scene_start_times,
        "cues": processed_cues
    }
    with open(TEMP / "acting_timings.json", "w", encoding="utf-8") as jf:
        json.dump(timings_data, jf, indent=2)

    # 1. Speech track yig'ish
    speech_track = np.zeros(total_samples, dtype=np.float32)
    speech_mask = np.zeros(total_samples, dtype=np.float32)

    for c in processed_cues:
        samples = load_audio_ffmpeg(c["file"], sr=sr)
        start_idx = int(c["start"] * sr)
        end_idx = min(total_samples, start_idx + len(samples))
        actual_len = end_idx - start_idx
        speech_track[start_idx:end_idx] += samples[:actual_len]
        # Ducking envelope
        speech_mask[start_idx:end_idx] = np.maximum(speech_mask[start_idx:end_idx], np.abs(samples[:actual_len]))

    # Ducking smoothing (attack 40ms, release 300ms)
    smooth_mask = np.zeros_like(speech_mask)
    curr = 0.0
    att = 1.0 / (0.04 * sr)
    rel = 1.0 / (0.30 * sr)
    for i in range(total_samples):
        target = min(1.0, speech_mask[i] * 3.5)
        if target > curr:
            curr = min(1.0, curr + att)
        else:
            curr = max(0.0, curr - rel)
        smooth_mask[i] = curr

    # 2. BGM ducking
    bgm_samples = load_audio_ffmpeg(bgm_wav, sr=sr)
    bgm_track = np.zeros(total_samples, dtype=np.float32)
    bgm_len = min(total_samples, len(bgm_samples))
    bgm_track[:bgm_len] = bgm_samples[:bgm_len]
    ducked_bgm = bgm_track * (1.0 - (smooth_mask * 0.80))

    # 3. SFX Track
    sfx_track = np.zeros(total_samples, dtype=np.float32)
    def add_sfx(sfx_path, at_sec, vol=1.0):
        if not os.path.exists(sfx_path):
            return
        s = load_audio_ffmpeg(sfx_path, sr=sr) * vol
        s_idx = int(at_sec * sr)
        e_idx = min(total_samples, s_idx + len(s))
        sfx_track[s_idx:e_idx] += s[:e_idx - s_idx]

    sfx_subbass = SFX_DIR / "sub_bass_impact.wav"
    sfx_whoosh = SFX_DIR / "whoosh.wav"
    sfx_click = SFX_DIR / "ui_click.wav"
    sfx_typing = SFX_DIR / "typing.wav"
    sfx_riser = SFX_DIR / "riser.wav"

    # SFX Event joylashuvi
    # 0s: Intro sub-bass
    add_sfx(sfx_subbass, 0.0, 1.1)
    # 1-sahna tugashi: typing sound
    add_sfx(sfx_typing, processed_cues[1]["start"], 0.8)

    # 2-sahna (Shok / Baza ketishi)
    sc2_start = scene_start_times[2]
    add_sfx(sfx_riser, max(0, sc2_start - 1.2), 0.8)
    add_sfx(sfx_subbass, sc2_start, 1.3)

    # 3-sahna (Telefon jiringlashi)
    sc3_start = scene_start_times[3]
    add_sfx(sfx_whoosh, sc3_start - 0.5, 0.9)
    # Telefon qo'ng'irog'i (double ring)
    add_sfx(sfx_click, sc3_start - 0.4, 1.4)
    add_sfx(sfx_click, sc3_start - 0.2, 1.4)

    # 4-sahna (StackOverflow)
    sc4_start = scene_start_times[4]
    add_sfx(sfx_whoosh, sc4_start, 0.9)
    add_sfx(sfx_typing, sc4_start + 0.5, 0.8)

    # 5-sahna (Fan / Rocket launch)
    sc5_start = scene_start_times[5]
    add_sfx(sfx_riser, max(0, sc5_start - 1.2), 0.9)
    add_sfx(sfx_subbass, sc5_start, 1.3)

    # 6-sahna (G'alaba va nuqta-vergul)
    sc6_start = scene_start_times[6]
    add_sfx(sfx_whoosh, sc6_start, 1.0)
    add_sfx(sfx_subbass, sc6_start + 1.2, 1.2)

    # 4. Master Mix
    final_mix = speech_track * 1.1 + ducked_bgm * 0.55 + sfx_track * 0.75
    # Outro fade
    fade_len = int(1.5 * sr)
    final_mix[-fade_len:] *= np.linspace(1, 0, fade_len)

    max_p = np.max(np.abs(final_mix))
    if max_p > 0.98:
        final_mix = final_mix / max_p * 0.96

    int_mix = (final_mix * 32767).astype(np.int16)

    master_wav = TEMP / "human_master_audio.wav"
    with wave.open(str(master_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(int_mix.tobytes())

    print(f"🎉 AKTYORLIK MASTER AUDIO TAYYOR ({total_duration:.2f}s): {master_wav}")

if __name__ == "__main__":
    main()
