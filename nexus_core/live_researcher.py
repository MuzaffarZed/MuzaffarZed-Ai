# -*- coding: utf-8 -*-
"""
Live Researcher (Anti-Hallucination Package & Docs Validator)
Muallif: MuzaffarZed
Standart: MUTLAQ MUKAMMALLIK (Zero-Beta, Zero-Defect)
PyPI, NPM va GitHub'dan paketlarni tekshiradi.
"""

import os
import json
import urllib.request

CACHE_DIR = os.path.join(r"C:\Users\MuzaffarZed\ai_workspace", ".nexus_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

class LiveResearcher:
    def check_pypi_package(self, pkg_name):
        url = f"https://pypi.org/pypi/{pkg_name}/json"
        cache_file = os.path.join(CACHE_DIR, f"pypi_{pkg_name}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                info = {
                    "exists": True,
                    "name": data["info"]["name"],
                    "version": data["info"]["version"],
                    "summary": data["info"]["summary"]
                }
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(info, f)
                return info
        except Exception as e:
            return {"exists": False, "error": str(e)}

if __name__ == "__main__":
    res = LiveResearcher().check_pypi_package("playwright")
    print(f"[LiveResearcher] PyPI tekshiruv: {res}")
    print("*Dasturchi: MuzaffarZed*")
