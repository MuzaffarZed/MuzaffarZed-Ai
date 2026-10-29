import zipfile
import re

apk_path = r'C:\Users\MuzaffarZed\ai_workspace\capcut_mod_lab\base.apk'
with zipfile.ZipFile(apk_path, 'r') as z:
    dex_files = [n for n in z.namelist() if n.endswith('.dex')]
    for dex_name in dex_files:
        data = z.read(dex_name)
        # Search for class names related to lvpro, settings, vip, proxy
        matches = set(re.findall(rb'Lcom/(?:bytedance/lvpro|lemon)/[a-zA-Z0-9_/$]*(?:Vip|VIP|Pro|proxy|Proxy|Setting|Config)[a-zA-Z0-9_/$]*;', data))
        if matches:
            print(f'=== {dex_name} matches ({len(matches)}) ===')
            for m in sorted(matches)[:10]:
                print(' ', m.decode('utf-8', errors='ignore'))
