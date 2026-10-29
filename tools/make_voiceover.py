import asyncio
import edge_tts
import os
import json

TEXT = "Tasavvur qiling: Agar siz qora o'raga tushib ketsangiz, siz uchun vaqt butunlay to'xtaydi! Tashqi dunyoda esa millionlab yillar bir soniyada o'tib ketadi. Bu — koinotning eng sirli mo'jizasidir!"

VOICE = "uz-UZ-SardorNeural"
OUTPUT_AUDIO = r"C:\Users\MuzaffarZed\ai_workspace\tools\voiceover.mp3"

async def generate_speech():
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="+5%", pitch="+0Hz")
    await communicate.save(OUTPUT_AUDIO)
    print(f"Generated voiceover: {OUTPUT_AUDIO}, size: {os.path.getsize(OUTPUT_AUDIO)} bytes")

if __name__ == "__main__":
    asyncio.run(generate_speech())
