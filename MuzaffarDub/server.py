"""
MuzaffarDub AI Voice Server
Muallif: Dasturchi MuzaffarZed
YouTube videolari uchun neyron real-vaqtli o'zbekcha ovozli dublyaj serveri.
"""

import os
import sys

# Windows cp1251 kodlash xatosidan mutlaq himoya
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import hashlib
import asyncio
from pathlib import Path
from typing import Optional
import urllib.parse
import aiohttp
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import uvicorn

APP_DIR = Path(__file__).parent.resolve()
CACHE_DIR = APP_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="MuzaffarDub Audio Engine",
    description="YouTube Real-time Uzbek Dubbing Engine by MuzaffarZed",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Original-Text", "X-Translated-Text", "X-Voice"]
)

VOICE_MAP = {
    "madina": "uz-UZ-MadinaNeural",
    "sardor": "uz-UZ-SardorNeural",
    "uz-uz-madinaneural": "uz-UZ-MadinaNeural",
    "uz-uz-sardorneural": "uz-UZ-SardorNeural"
}

# Tarjima xotirasi (Memory cache)
TRANSLATION_CACHE = {}

async def translate_to_uzbek(text: str, source_lang: str = "auto") -> str:
    """O'zbek tiliga tezkor va aniq tarjima qilish (MyMemory + Google fallback)."""
    text = text.strip()
    if not text:
        return ""

    if text in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[text]

    encoded = urllib.parse.quote(text)
    
    # 1. MyMemory Bepul API (Yuqori aniqlikdagi o'zbekcha)
    src_pair = "en" if source_lang == "auto" else source_lang
    url_mm = f"https://api.mymemory.translated.net/get?q={encoded}&langpair={src_pair}|uz"
    try:
        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            async with session.get(url_mm, timeout=4) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    translated = data.get("responseData", {}).get("translatedText")
                    if translated and not translated.startswith("MYMEMORY WARNING"):
                        TRANSLATION_CACHE[text] = translated
                        return translated
    except Exception:
        pass

    # 2. Google Translate Fallback
    url_gtx = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl=uz&dt=t&q={encoded}"
    try:
        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}) as session:
            async with session.get(url_gtx, timeout=3) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    translated = "".join([segment[0] for segment in data[0] if segment and segment[0]])
                    if translated:
                        TRANSLATION_CACHE[text] = translated
                        return translated
    except Exception:
        pass

    # Agar tarjima bo'lmasa, matnning o'zi
    return text

@app.get("/")
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "MuzaffarDub Engine",
        "developer": "MuzaffarZed",
        "default_voice": "uz-UZ-MadinaNeural",
        "supported_voices": list(VOICE_MAP.keys()),
        "cached_audios": len(list(CACHE_DIR.glob("*.mp3"))),
        "cached_translations": len(TRANSLATION_CACHE)
    }

@app.get("/translate")
async def translate_endpoint(
    text: str = Query(..., description="Tarjima qilinadigan matn"),
    source: str = Query("auto", description="Boshlang'ich til")
):
    translated = await translate_to_uzbek(text, source)
    return {
        "original": text,
        "translated": translated,
        "source": source,
        "target": "uz"
    }

@app.get("/tts")
async def tts_endpoint(
    text: str = Query(..., description="Ovozlashtiriladigan matn"),
    voice: str = Query("madina", description="madina yoki sardor"),
    rate: str = Query("+0%", description="Tezlik: masalan +10% yoki +20%")
):
    """Tayyor matnni Microsoft Edge Neural ovozi bilan sintez qilish."""
    text_clean = text.strip()
    if not text_clean:
        raise HTTPException(status_code=400, detail="Matn bo'sh bo'lishi mumkin emas")

    selected_voice = VOICE_MAP.get(voice.lower().strip(), "uz-UZ-MadinaNeural")

    cache_key = hashlib.sha256(f"{selected_voice}_{rate}_{text_clean}".encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.mp3"

    if cache_file.exists() and cache_file.stat().st_size > 0:
        return Response(content=cache_file.read_bytes(), media_type="audio/mpeg")

    try:
        communicate = edge_tts.Communicate(text=text_clean, voice=selected_voice, rate=rate)
        audio_buffer = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.extend(chunk["data"])

        if not audio_buffer:
            raise HTTPException(status_code=500, detail="Audio hosil bo'lmadi")

        audio_bytes = bytes(audio_buffer)
        cache_file.write_bytes(audio_bytes)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"TTS xatoligi: {str(err)}")

@app.get("/dub")
async def dub_endpoint(
    text: str = Query(..., description="Subtitr matni"),
    is_uzbek: bool = Query(False, description="Matn allaqachon o'zbekchami"),
    voice: str = Query("madina", description="madina yoki sardor"),
    rate: str = Query("+10%", description="Dublyaj tezligi")
):
    """1-bosqichda tarjima qilish va audio sintez qilish (Eng tezkor 1-Click Dublyaj)."""
    text_clean = text.strip()
    if not text_clean:
        raise HTTPException(status_code=400, detail="Matn bo'sh")

    # 1. Agar o'zbekcha bo'lmasa, tarjima qilamiz
    if is_uzbek:
        uzbek_text = text_clean
    else:
        uzbek_text = await translate_to_uzbek(text_clean)

    # 2. Ovoz hosil qilamiz
    selected_voice = VOICE_MAP.get(voice.lower().strip(), "uz-UZ-MadinaNeural")
    cache_key = hashlib.sha256(f"{selected_voice}_{rate}_{uzbek_text}".encode("utf-8")).hexdigest()
    cache_file = CACHE_DIR / f"{cache_key}.mp3"

    if cache_file.exists() and cache_file.stat().st_size > 0:
        audio_bytes = cache_file.read_bytes()
    else:
        try:
            communicate = edge_tts.Communicate(text=uzbek_text, voice=selected_voice, rate=rate)
            audio_buffer = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.extend(chunk["data"])
            audio_bytes = bytes(audio_buffer)
            cache_file.write_bytes(audio_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Dublyaj sintez xatosi: {str(e)}")

    headers = {
        "X-Original-Text": urllib.parse.quote(text_clean[:200]),
        "X-Translated-Text": urllib.parse.quote(uzbek_text[:200]),
        "X-Voice": selected_voice
    }
    return Response(content=audio_bytes, media_type="audio/mpeg", headers=headers)

if __name__ == "__main__":
    print("=" * 65)
    print("[*] MuzaffarDub AI Voice Server ishga tushdi!")
    print("[*] Dasturchi: MuzaffarZed")
    print("[*] Manzil: http://127.0.0.1:8989")
    print("=" * 65)
    uvicorn.run(app, host="127.0.0.1", port=8989, log_level="warning")
