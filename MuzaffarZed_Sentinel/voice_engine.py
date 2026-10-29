import os
import asyncio
import threading
import edge_tts
import pygame

VOICE_DIR = os.path.expanduser(r"~\AppData\Local\Temp\muzaffarzed_voice")
os.makedirs(VOICE_DIR, exist_ok=True)

DEFAULT_VOICE = "uz-UZ-SardorNeural"

def init_audio():
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except Exception as e:
        print("Audio init error:", e)

async def _synthesize(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)

def speak(text, voice=DEFAULT_VOICE, blocking=False):
    """
    Synthesizes and speaks Uzbek text asynchronously.
    """
    def _run():
        try:
            init_audio()
            out_path = os.path.join(VOICE_DIR, f"speech_{abs(hash(text)) % 100000}.mp3")
            asyncio.run(_synthesize(text, voice, out_path))
            if os.path.exists(out_path):
                pygame.mixer.music.load(out_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and blocking:
                    pygame.time.Clock().tick(10)
        except Exception as e:
            print("Voice error:", e)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    if blocking:
        t.join()

if __name__ == "__main__":
    print("Testing Voice Engine with Sardor Neural...")
    speak("Assalomu alaykum, muhtaram janob Muzaffar! Ovozli tizim faollashtirildi.", blocking=True)
    print("Voice test finished successfully!")
