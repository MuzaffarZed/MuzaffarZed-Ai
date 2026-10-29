# -*- coding: utf-8 -*-
import os
import sys
import json
import urllib.request
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def inspect_lblink():
    url = "http://192.168.16.1/cgi-bin/luci/;stok=888f163d2148d8c8ae6c218b60b56fae/admin/opsw/main.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        print("=== LB-LINK HTML Length ===", len(html))
        scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html)
        print("Loaded Scripts:", scripts)
        # Find inline scripts
        inlines = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
        for i, code in enumerate(inlines):
            print(f"--- Inline Script #{i+1} ---")
            print(code.strip()[:600])
    except Exception as e:
        print("LB-LINK error:", e)

def inspect_innbox():
    url = "http://192.168.1.1/old_login.htm"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        print("\n=== Innbox G74L HTML Length ===", len(html))
        # Look for form action
        form_actions = re.findall(r'<form[^>]+action=[\'"]([^\'"]+)[\'"]', html, re.I)
        print("Form Actions:", form_actions)
        # Look for buttons / titles
        inputs = re.findall(r'<input[^>]+>', html, re.I)
        print(f"Total Inputs: {len(inputs)}")
        for inp in inputs:
            print(" ", inp.strip())
    except Exception as e:
        print("Innbox error:", e)

if __name__ == "__main__":
    inspect_lblink()
    inspect_innbox()
