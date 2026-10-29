import traceback
import sys

with open("C:/Users/MuzaffarZed/ai_workspace/MuzaffarDub/crash.log", "w", encoding="utf-8") as f:
    try:
        from server import app
        import uvicorn
        f.write("Starting uvicorn...\n")
        f.flush()
        uvicorn.run(app, host="127.0.0.1", port=8989, log_level="debug")
    except Exception as e:
        f.write("EXCEPTION: " + str(e) + "\n")
        f.write(traceback.format_exc() + "\n")
        f.flush()
