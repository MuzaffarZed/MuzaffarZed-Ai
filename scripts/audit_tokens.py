import os
import re
from pathlib import Path
from collections import defaultdict

home = Path.home()
workspace = Path(r"C:\Users\MuzaffarZed\ai_workspace")

sources = [
    ("gemini_skills", home / ".gemini" / "skills"),
    ("gemini_config_skills", home / ".gemini" / "config" / "skills"),
    ("home_agents_skills", home / ".agents" / "skills"),
    ("workspace_skills", workspace / ".agents" / "skills"),
    ("plugins", home / ".gemini" / "config" / "plugins")
]

skills_found = {}
total_desc_chars = 0
unique_names = set()

for src_name, s in sources:
    if not s.exists():
        continue
    for root, dirs, files in os.walk(s):
        if "SKILL.md" in files:
            p = Path(root) / "SKILL.md"
            content = p.read_text(encoding="utf-8", errors="ignore")
            # extract description
            m = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            desc = ""
            if m:
                for line in m.group(1).split("\n"):
                    if line.strip().startswith("description:"):
                        desc = line.split("description:", 1)[1].strip()
                        break
            name = Path(root).name
            unique_names.add(name)
            skills_found[str(p)] = {"name": name, "source": src_name, "desc": desc}
            total_desc_chars += len(content)

print(f"Total SKILL.md files across all locations: {len(skills_found)}")
print(f"Unique skill names: {len(unique_names)}")
print(f"Total characters of all SKILL.md files: {total_desc_chars}")
