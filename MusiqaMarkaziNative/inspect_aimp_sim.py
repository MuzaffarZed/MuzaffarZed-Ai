import sys, os
sys.stdout.reconfigure(encoding='utf-8')

base = r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative'
html_path = os.path.join(base, 'ui', 'index.html')

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

import re
aimp_match = re.search(r'(<section id="tab-aimp".*?</section>)', text, re.DOTALL)
if aimp_match:
    print("AIMP section length:", len(aimp_match.group(1)))
    lines = aimp_match.group(1).splitlines()
    print("AIMP first 30 lines:")
    for l in lines[:30]:
        print(l)

sim_match = re.search(r'(<section id="tab-simulator".*?</section>)', text, re.DOTALL)
if sim_match:
    print("\nSIMULATOR section length:", len(sim_match.group(1)))
    lines = sim_match.group(1).splitlines()
    print("SIMULATOR first 30 lines:")
    for l in lines[:30]:
        print(l)
