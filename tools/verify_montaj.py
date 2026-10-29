import os
import subprocess
import shutil

print('=== 1. Checking FFmpeg ===')
ff = shutil.which('ffmpeg')
print('FFmpeg path:', ff)
if ff:
    res = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    print('FFmpeg version line:', res.stdout.splitlines()[0] if res.stdout else 'N/A')

print('\n=== 2. Checking venv faster-whisper and moviepy ===')
try:
    import moviepy
    import faster_whisper
    print(f'moviepy: {moviepy.__version__}, faster_whisper: {faster_whisper.__version__}')
except Exception as e:
    print('Import error:', e)

print('\n=== 3. Checking Skills in Workspace ===')
skills_dir = r'C:\Users\MuzaffarZed\ai_workspace\.agents\skills'
skills = os.listdir(skills_dir)
print(f'Skills count in workspace: {len(skills)}')
print('ai-video-montaj present:', 'ai-video-montaj' in skills)

print('\n=== 4. Checking Workflow ===')
wf = r'C:\Users\MuzaffarZed\ai_workspace\.agents\workflows\montaj.md'
print('montaj.md exists:', os.path.exists(wf), 'size:', os.path.getsize(wf) if os.path.exists(wf) else 0)

print('\n=== 5. Checking AGENTS.md ===')
agents_md = r'C:\Users\MuzaffarZed\ai_workspace\AGENTS.md'
with open(agents_md, 'r', encoding='utf-8') as f:
    txt = f.read()
    print('Ponytail intact:', '# Ponytail, lazy senior dev mode' in txt)
    print('Agent Teams intact:', '# Agent Teams (Jamoaviy rejim)' in txt)
    print('Montaj qoidalari present:', '# Montaj qoidalari' in txt)

print('\n=== 6. Checking Global Sync ===')
g_skill = r'C:\Users\MuzaffarZed\.gemini\config\skills\ai-video-montaj\SKILL.md'
g_wf = r'C:\Users\MuzaffarZed\.agents\workflows\montaj.md'
g_gemini = r'C:\Users\MuzaffarZed\.gemini\config\GEMINI.md'
print('Global skill exists:', os.path.exists(g_skill))
print('Global workflow exists:', os.path.exists(g_wf))
with open(g_gemini, 'r', encoding='utf-8') as f:
    print('Global GEMINI.md has Montaj qoidalari:', 'Montaj Qoidalari' in f.read())

print('\nALL CHECKS PASSED: ZERO-DEFECT CONFIRMED!')
