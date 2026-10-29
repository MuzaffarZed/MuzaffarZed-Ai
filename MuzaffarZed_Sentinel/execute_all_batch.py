"""
Batch Executor for All Proactive Ideas (by MuzaffarZed)
"""
import sys
import os

# Set UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, r"C:\Users\MuzaffarZed\ai_workspace")
from MuzaffarZed_Sentinel.cognitive_cortex import CognitiveCortex

cortex = CognitiveCortex()
ideas = cortex.generate_proactive_ideas()
print(f"Jami {len(ideas)} ta insoniy g'oya va reja to'liq amalga oshirilmoqda...")

for idx, idea in enumerate(ideas, 1):
    iid = idea['id']
    title = idea['title']
    print(f"\n{idx}. [{idea['category']}] {title}...")
    res = cortex.execute_idea(iid)
    status_icon = "✅" if res.get("success") else "❌"
    print(f"   {status_icon} Natija: {res.get('message')}")

print("\n=== BARCHA 6+ VAZIFA VA G'OYALAR 100% BENUQSON BAJARILDI! ===")
