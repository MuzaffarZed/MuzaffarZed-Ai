import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\LocalStudioServer.cs', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'if\s*\((?:req\.Url\.AbsolutePath|path)\s*==\s*"(/api/[^"]+)"\)', text)
print("API Routes in LocalStudioServer.cs:")
for r in m:
    print(" -", r)
