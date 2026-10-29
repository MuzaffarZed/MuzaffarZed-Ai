import os

with open(r'C:\Users\MuzaffarZed\Downloads\system_packages.txt', 'r', encoding='utf-8') as f:
    packages = [line.strip().replace('package:', '') for line in f if line.strip()]

# Safe to remove bloat patterns for Samsung One UI Core
bloat_keywords = [
    'bixby', 'diagmon', 'scloud', 'game', 'kids', 'rubin', 'mdx', 'allshare',
    'knox', 'skydrive', 'office', 'feedback', 'tachyon', 'partner',
    'livewallpaper', 'sticker', 'avatar', 'aremoji', 'arzone', 'antradio',
    'print', 'fido', 'fota', 'omc', 'appupdate', 'samsung.android.ipsgeofence',
    'samsung.android.authfw', 'samsung.android.spay', 'samsung.android.dynamiclock',
    'samsung.android.easysetup', 'sec.android.app.billing', 'samsung.android.mobileservice',
    'sec.spp.push', 'samsung.android.beaconmanager', 'samsung.android.aware.service',
    'samsung.android.smartcallprovider', 'samsung.android.app.spage', 'samsung.android.mcfds',
    'samsung.android.mcfserver', 'samsung.android.app.sharelive', 'samsung.android.visualbars'
]

targets = []
for p in packages:
    for kw in bloat_keywords:
        if kw in p.lower():
            targets.append(p)
            break

targets = sorted(list(set(targets)))
print(f"Identified {len(targets)} bloatware packages.")
with open(r'C:\Users\MuzaffarZed\Downloads\debloat_list.txt', 'w', encoding='utf-8') as out:
    for t in targets:
        out.write(t + '\n')
