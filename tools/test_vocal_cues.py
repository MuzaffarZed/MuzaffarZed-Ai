import asyncio
import edge_tts
import subprocess
from pathlib import Path

TEMP = Path(r"C:\Users\MuzaffarZed\ai_workspace\pro-video-engine\temp_vocal_test")
TEMP.mkdir(parents=True, exist_ok=True)

test_cues = [
    ("cue1.mp3", "uz-UZ-SardorNeural", "-2%", "-1Hz", "Kechki soat sakkiz... Oshxona tinch, hamma maza qilib choy ichyapti."),
    ("cue2.mp3", "uz-UZ-SardorNeural", "+8%", "+2Hz", "Bizning dasturchi esa: Bo'ldi! Hozir bitta tugmani ko'k qilib qo'yaman-u, maza qilib uxlayman, dedi!"),
    ("cue3.mp3", "uz-UZ-SardorNeural", "-5%", "-2Hz", "Eh birodar... Eng katta fojialar aynan mana shu gapdan boshlanadi..."),
]

async def gen():
    for f, v, r, p, text in test_cues:
        out = TEMP / f
        c = edge_tts.Communicate(text, v, rate=r, pitch=p)
        await c.save(str(out))
        print(f"Generated {f}")

asyncio.run(gen())
