"""
JARVIS AI Singing Studio - FastAPI Server
Master Architect: janob Muzaffar uchun yagona AI vokal va qo'shiq yaratish studiyasi backend serveri.
"""

import datetime
import logging
import os
import shutil
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
import sys
from pathlib import Path

# Asosiy yo'llar
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

try:
    from core.audio_engine import AudioEngine, AudioEngineError
    from core.stem_separator import StemSeparator
    from core.voice_converter import VoiceConverter
    from core.voice_manager import VoiceManager
except ImportError:
    from singing_studio.core.audio_engine import AudioEngine, AudioEngineError
    from singing_studio.core.stem_separator import StemSeparator
    from singing_studio.core.voice_converter import VoiceConverter
    from singing_studio.core.voice_manager import VoiceManager

# Logging sozlamalari (Windows cp1251 xavfsiz formatda)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("SingingStudio")

# Asosiy yo'llar
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_TEMP = DATA_DIR / "temp"
OUTPUT_DIR = DATA_DIR / "output"
UPLOAD_TEMP.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Tizim komponentlari
audio_engine = AudioEngine()
voice_manager = VoiceManager(data_root=DATA_DIR)
stem_separator = StemSeparator(data_root=DATA_DIR)
voice_converter = VoiceConverter(data_root=DATA_DIR)

app = FastAPI(
    title="JARVIS AI Singing Studio",
    description="Janob Muzaffar uchun yagona AI Vokal va Qo'shiq Studiyasi",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static va Templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/status")
async def get_system_status():
    """Tizim holati va tayyorlik parametrlarini qaytaradi."""
    stats = voice_manager.get_dataset_statistics()
    models = voice_manager.list_models()
    return {
        "status": "online",
        "system": "JARVIS AI Singing Studio",
        "architect": "janob Muzaffar",
        "ffmpeg_ready": True,
        "dataset_stats": stats,
        "models_count": len(models),
        "active_models": models
    }


# ==================== OVOZ BOSHQARUVI (VOICE DATASET & MODELS) ====================

@app.post("/api/voice/record")
async def record_voice(file: UploadFile = File(...)):
    """Mikrofondan yozib olingan ovoz faylini qabul qilib tozalaydi."""
    try:
        temp_file = UPLOAD_TEMP / f"rec_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = voice_manager.add_voice_sample(temp_file)
        if temp_file.exists():
            temp_file.unlink()

        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        logger.error(f"Ovoz yozishda xatolik: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/upload")
async def upload_voice(file: UploadFile = File(...)):
    """Foydalanuvchi kompyuteridan ovoz faylini yuklaydi."""
    try:
        ext = Path(file.filename or "voice.wav").suffix or ".wav"
        temp_file = UPLOAD_TEMP / f"upload_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = voice_manager.add_voice_sample(temp_file, custom_name=file.filename)
        if temp_file.exists():
            temp_file.unlink()

        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        logger.error(f"Ovoz yuklashda xatolik: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voice/samples")
async def get_voice_samples():
    """Barcha tozalangan ovoz namunalari ro'yxati va statistikasi."""
    samples = voice_manager.list_voice_samples()
    stats = voice_manager.get_dataset_statistics()
    return {"samples": samples, "stats": stats}


@app.delete("/api/voice/sample/{filename}")
async def delete_voice_sample(filename: str):
    """Ovoz namunasini o'chiradi."""
    success = voice_manager.delete_sample(filename)
    return {"success": success}


@app.get("/api/voice/package-zip")
async def download_dataset_zip():
    """Colab-da o'qitish uchun ovozlar to'plamini ZIP arxiv qilib beradi."""
    try:
        zip_path = voice_manager.package_dataset_zip()
        return FileResponse(
            path=str(zip_path),
            filename="muzaffar_voice_dataset.zip",
            media_type="application/zip"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/voice/models")
async def list_models():
    """Mavjud AI ovoz modellari."""
    return {"models": voice_manager.list_models()}


@app.post("/api/voice/model/upload")
async def upload_model(file: UploadFile = File(...), index_file: Optional[UploadFile] = File(None)):
    """O'qitilgan .pth model va .index faylini tizimga yuklaydi."""
    try:
        model_temp = UPLOAD_TEMP / file.filename
        with open(model_temp, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        index_temp = None
        if index_file:
            index_temp = UPLOAD_TEMP / index_file.filename
            with open(index_temp, "wb") as buf:
                shutil.copyfileobj(index_file.file, buf)

        res = voice_manager.add_model(model_temp, index_temp)

        if model_temp.exists():
            model_temp.unlink()
        if index_temp and index_temp.exists():
            index_temp.unlink()

        return {"success": True, "model": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== QO'SHIQ VA MINUSOVKA BOSHQARUVI ====================

@app.post("/api/song/upload-track")
async def upload_song_track(file: UploadFile = File(...), track_type: str = Form("song")):
    """
    To'liq qo'shiq, yoki alohida minusovka / vokal faylini yuklaydi.
    track_type: 'song', 'minus', 'vocal'
    """
    try:
        ext = Path(file.filename or "track.mp3").suffix or ".mp3"
        safe_name = f"{track_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        target_path = DATA_DIR / "songs" / safe_name
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        info = audio_engine.get_audio_info(target_path)
        return {
            "success": True,
            "filename": safe_name,
            "track_type": track_type,
            "path": str(target_path),
            "duration": info["duration"],
            "duration_formatted": info["duration_formatted"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/song/separate")
async def separate_stems(song_filename: str = Form(...)):
    """To'liq qo'shiqdan vokal va minusovkani ajratadi."""
    try:
        song_path = DATA_DIR / "songs" / song_filename
        if not song_path.exists():
            raise HTTPException(status_code=404, detail="Qo'shiq fayli topilmadi")

        stems = stem_separator.separate_song(song_path)
        return {
            "success": True,
            "vocals": Path(stems["vocals"]).name,
            "instrumental": Path(stems["instrumental"]).name
        }
    except Exception as e:
        logger.error(f"Stem separation xatosi: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ASOSIY YARATISH (STUDIO RENDER) ====================

@app.post("/api/render")
async def render_final_song(
    vocal_file: str = Form(...),
    minus_file: str = Form(...),
    model_name: str = Form("default"),
    pitch_shift: float = Form(0.0),
    vocal_vol: float = Form(1.0),
    minus_vol: float = Form(0.9),
    reverb: float = Form(0.25),
    echo: float = Form(0.0),
    apply_mastering: bool = Form(True)
):
    """
    Barcha komponentlarni birlashtirib, tayyor qo'shiqni yaratadi:
    1. Vokalni Janob Muzaffar ovoziga va tanlangan pitch toniga o'giradi
    2. Reverb va vokal studiya effektlarini qo'llaydi
    3. Minusovka bilan sinxron birlashtiradi
    4. EBU R128 mastering orqali professional studiya darajasiga chiqaradi
    """
    try:
        # Vokal va minus yo'llarini aniqlaymiz
        voc_path = DATA_DIR / "songs" / vocal_file
        min_path = DATA_DIR / "songs" / minus_file

        if not voc_path.exists():
            # Balki output papkadadir
            voc_path = OUTPUT_DIR / vocal_file
        if not min_path.exists():
            min_path = OUTPUT_DIR / minus_file

        if not voc_path.exists():
            raise HTTPException(status_code=404, detail=f"Vokal fayli topilmadi: {vocal_file}")
        if not min_path.exists():
            raise HTTPException(status_code=404, detail=f"Minusovka fayli topilmadi: {minus_file}")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        conv_vocal_name = f"ai_vocal_{timestamp}.wav"
        final_song_name = f"tayyor_qoshiq_{timestamp}.mp3"
        final_output_path = OUTPUT_DIR / final_song_name

        logger.info(f"Qo'shiq yaratilmoqda: Pitch={pitch_shift}, Reverb={reverb}, Mastering={apply_mastering}")

        # 1. AI Vokal Konvertatsiyasi & Pitch Shift
        conv_res = voice_converter.convert_vocal(
            guide_vocal_path=voc_path,
            pitch_shift=pitch_shift,
            reverb_level=reverb,
            echo_level=echo,
            output_name=conv_vocal_name
        )

        converted_vocal_path = conv_res["converted_vocal_path"]

        # 2. Studiya Mikseri va Mastering
        audio_engine.mix_song(
            vocal_path=converted_vocal_path,
            minus_path=min_path,
            output_path=final_output_path,
            vocal_vol=vocal_vol,
            minus_vol=minus_vol,
            apply_mastering=apply_mastering
        )

        info = audio_engine.get_audio_info(final_output_path)

        return {
            "success": True,
            "output_filename": final_song_name,
            "play_url": f"/api/audio/stream/{final_song_name}",
            "download_url": f"/api/audio/download/{final_song_name}",
            "duration": info["duration"],
            "duration_formatted": info["duration_formatted"],
            "bitrate": "320 kbps (Studio Master)"
        }
    except Exception as e:
        logger.error(f"Render jarayonida xatolik: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== AUDIO PLEER VA YUKLAB OLISH ====================

@app.get("/api/audio/stream/{filename}")
async def stream_audio(filename: str):
    """Audio faylni brauzerda tinglash uchun oqim (stream) tarzida uzatadi."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        file_path = DATA_DIR / "songs" / filename
    if not file_path.exists():
        file_path = DATA_DIR / "voices" / "cleaned" / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio fayl topilmadi")

    media_type = "audio/mpeg" if file_path.suffix.lower() == ".mp3" else "audio/wav"
    return FileResponse(path=str(file_path), media_type=media_type)


@app.get("/api/audio/download/{filename}")
async def download_audio(filename: str):
    """Tayyor qo'shiqni kompyuterga yuklab olish."""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fayl topilmadi")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )


def start_server(host: str = "127.0.0.1", port: int = 7860):
    """Studiyani ishga tushirish funktsiyasi."""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
