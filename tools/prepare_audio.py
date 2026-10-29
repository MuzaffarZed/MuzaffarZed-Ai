import subprocess
import json
import os
import numpy as np

def prepare_audio_and_words():
    # 1. Original words from words.json
    with open(r"C:\Users\MuzaffarZed\ai_workspace\tools\words.json", "r", encoding="utf-8") as f:
        raw_words = json.load(f)

    # Clean words and match with proper Uzbek text
    # Sentence 1: Tasavvur qiling: Agar siz qora o'raga tushib ketsangiz, siz uchun vaqt butunlay to'xtaydi!
    # Sentence 2: Tashqi dunyoda esa millionlab yillar bir soniyada o'tib ketadi.
    # Sentence 3: Bu — koinotning eng sirli mo'jizasidir!

    # Pauses detected: 4.89 to 5.71 (dur 0.82s), 8.85 to 9.67 (dur 0.82s), 11.82 to end (dur 0.78s)
    keep_segments = [
        {"start": 0.0, "end": 4.89},
        {"start": 5.71, "end": 8.85},
        {"start": 9.67, "end": 11.82}
    ]

    # Map words to cut timeline
    mapped_words = []
    # Clean text representation
    clean_words = [
        "Tasavvur", "qiling:", "Agar", "siz", "qora", "o'raga", "tushib", "ketsangiz,",
        "siz", "uchun", "vaqt", "butunlay", "to'xtaydi!",
        "Tashqi", "dunyoda", "esa", "millionlab", "yillar", "bir", "soniyada", "o'tib", "ketadi.",
        "Bu —", "koinotning", "eng", "sirli", "mo'jizasidir!"
    ]

    # Cut audio via FFmpeg
    input_audio = r"C:\Users\MuzaffarZed\ai_workspace\tools\voiceover.mp3"
    cut_voice = r"C:\Users\MuzaffarZed\ai_workspace\tools\voice_cut.wav"
    
    filter_parts = []
    for i, seg in enumerate(keep_segments):
        filter_parts.append(f"[0:a]atrim=start={seg['start']}:end={seg['end']},asetpts=PTS-STARTPTS[a{i}]")
    concat_filter = "".join(f"[a{i}]" for i in range(len(keep_segments))) + f"concat=n={len(keep_segments)}:v=0:a=1[outa]"
    full_filter = ";".join(filter_parts) + ";" + concat_filter

    cmd = [
        "ffmpeg", "-y", "-i", input_audio,
        "-filter_complex", full_filter,
        "-map", "[outa]",
        "-ar", "44100", "-ac", "2",
        cut_voice
    ]
    subprocess.run(cmd, check=True)
    print("Cut voice audio created:", cut_voice)

    # Get total cut audio duration
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", cut_voice]
    total_dur = float(subprocess.check_output(dur_cmd).strip())
    print("Total cut audio duration:", total_dur, "seconds")

    # Generate cosmic ambient music
    ambient_wav = r"C:\Users\MuzaffarZed\ai_workspace\tools\ambient.wav"
    sample_rate = 44100
    t = np.linspace(0, total_dur, int(sample_rate * total_dur), endpoint=False)
    # Layered cosmic pad: 55Hz (A1), 110Hz (A2), 165Hz (E3), 220Hz (A3), with slow frequency modulation
    drone = (
        0.35 * np.sin(2 * np.pi * 55 * t) +
        0.25 * np.sin(2 * np.pi * 110 * t + 0.1 * np.sin(2 * np.pi * 0.2 * t)) +
        0.18 * np.sin(2 * np.pi * 165 * t + 0.1 * np.cos(2 * np.pi * 0.3 * t)) +
        0.12 * np.sin(2 * np.pi * 220 * t) +
        0.05 * np.random.normal(0, 0.1, len(t)) # subtle space cosmic hiss
    )
    # Fade in / fade out envelope
    fade_len = int(sample_rate * 0.5)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    drone[:fade_len] *= fade_in
    drone[-fade_len:] *= fade_out

    # Save ambient wav
    from scipy.io import wavfile
    wavfile.write(ambient_wav, sample_rate, (drone * 32767).astype(np.int16))

    # Mix voice + ambient: voice volume 1.0, ambient volume 0.15
    final_audio = r"C:\Users\MuzaffarZed\ai_workspace\tools\final_audio.wav"
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", cut_voice,
        "-i", ambient_wav,
        "-filter_complex", "[0:a]volume=1.0[v];[1:a]volume=0.2[bg];[v][bg]amix=inputs=2:duration=first[out]",
        "-map", "[out]",
        final_audio
    ]
    subprocess.run(mix_cmd, check=True)
    print("Final mixed audio created:", final_audio)

    return total_dur

if __name__ == "__main__":
    dur = prepare_audio_and_words()
    print("Audio preparation done. Duration:", dur)
