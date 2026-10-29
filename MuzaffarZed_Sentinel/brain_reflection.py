import os
import json
from datetime import datetime

REFLECTION_FILE = os.path.expanduser(r"~/.gemini/config/muzaffarzed_reflection.json")

DEFAULT_REFLECTIONS = {
    "system_identity": "MuzaffarZed Autonomous Master AI",
    "master_architect": "janob Muzaffar",
    "total_reflections": 3,
    "rules_discovered": [
        {
            "id": "RULE-01",
            "title": "Visual Grounding Mandatory",
            "lesson": "Never declare task complete based on assumption. Always capture screen and verify icons and windows with eyes.",
            "discovered_at": "2026-10-17T13:12:00"
        },
        {
            "id": "RULE-02",
            "title": "Zero Cartoon Games Policy",
            "lesson": "Janob Muzaffar dislikes cartoon/baby 2D games (Zuma, Panda, PvZ). Only modern, serious 3D games must be on Desktop.",
            "discovered_at": "2026-10-17T12:08:00"
        },
        {
            "id": "RULE-03",
            "title": "PowerShell Non-Interactive Immunity",
            "lesson": "Never run multi-line or unquoted powershell commands in cmd. They wait on interactive stdin and hang for hours. Always use Python scripts or -NonInteractive flags.",
            "discovered_at": "2026-10-17T14:03:00"
        }
    ],
    "experience_journal": [
        {
            "task": "Game dependency repair (0xc0000135)",
            "solution": "Extracted DirectX 9 CABs (d3dx9_42.dll, xinput1_3.dll) and VC++ 2008 (msvcr90.dll) directly into application directory.",
            "outcome": "100% Success. Mafia 2, Blur, Saints Row 3 launched cleanly."
        },
        {
            "task": "White broken icon removal",
            "solution": "Inspected both User Desktop and Public Desktop. Removed broken GOG Firewatch.lnk from C:\\Users\\Public\\Desktop.",
            "outcome": "100% Success. Replaced with official lookout tower icon."
        }
    ]
}

def load_reflections():
    if os.path.exists(REFLECTION_FILE):
        try:
            with open(REFLECTION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    save_reflections(DEFAULT_REFLECTIONS)
    return DEFAULT_REFLECTIONS

def save_reflections(data):
    os.makedirs(os.path.dirname(REFLECTION_FILE), exist_ok=True)
    with open(REFLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def record_experience(task, solution, outcome):
    data = load_reflections()
    entry = {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "solution": solution,
        "outcome": outcome
    }
    data["experience_journal"].append(entry)
    data["total_reflections"] = len(data["experience_journal"])
    save_reflections(data)
    print(f"Recorded reflection: {task} -> {outcome}")

def consult_experience(keyword):
    """
    Looks up previous wisdom and lessons learned matching keyword.
    """
    data = load_reflections()
    keyword = keyword.lower()
    matches = []
    for r in data.get("rules_discovered", []):
        if keyword in r["title"].lower() or keyword in r["lesson"].lower():
            matches.append(f"[{r['id']}] {r['title']}: {r['lesson']}")
    for exp in data.get("experience_journal", []):
        if keyword in exp["task"].lower() or keyword in exp["solution"].lower():
            matches.append(f"[EXP] {exp['task']} -> {exp['solution']}")
    return matches

if __name__ == "__main__":
    print("Initializing MuzaffarZed Reflection Engine...")
    ref = load_reflections()
    print("Total Rules discovered:", len(ref["rules_discovered"]))
    print("Total Experiences logged:", len(ref["experience_journal"]))
    test_lookup = consult_experience("powershell")
    print("\nLookup 'powershell':", test_lookup)
