import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

script = """
for f in /storage/3EF8-7461/*/GUI/*_000.png; do
    echo "$f:"
    head -c 16 "$f" | od -t x1
    break
done
"""
with open("C:/Users/MuzaffarZed/ai_workspace/tmp_check.sh", "w", encoding="utf-8") as f:
    f.write(script)
subprocess.run([adb, "push", "C:/Users/MuzaffarZed/ai_workspace/tmp_check.sh", "/data/local/tmp/tmp_check.sh"], capture_output=True)
r = subprocess.run([adb, "shell", "su", "0", "sh", "/data/local/tmp/tmp_check.sh"], capture_output=True, text=True, timeout=10)
print(r.stdout.strip())
