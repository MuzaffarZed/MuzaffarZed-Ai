import urllib.request
import re
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def get_html(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode('utf-8', errors='ignore')

url1 = "https://www.apkmirror.com/apk/samsung-electronics-co-ltd/gimbal-subject-tracking/gimbal-subject-tracking-2-0-00-8-release/"
print("1-bosqich: Sahifa yuklanmoqda...")
html1 = get_html(url1)

# Step 1: find release page or direct download page
# Link to download page:
match1 = re.search(r'href="(/apk/samsung-electronics-co-ltd/gimbal-subject-tracking/[^"]*download/[^"]*)"', html1)
if not match1:
    match1 = re.search(r'href="([^"]*download[^"]*)"', html1)

if not match1:
    print("Download sahifasi topilmadi!")
    sys.exit(1)

url2 = "https://www.apkmirror.com" + match1.group(1) if match1.group(1).startswith("/") else match1.group(1)
print(f"2-bosqich: {url2} yuklanmoqda...")
html2 = get_html(url2)

# Step 2: find download button
match2 = re.search(r'href="(/apk/samsung-electronics-co-ltd/gimbal-subject-tracking/[^"]*key=[^"]*)"', html2)
if not match2:
    match2 = re.search(r'href="([^"]*wp-content/themes/responsive/download\.php[^"]*)"', html2)

if match2:
    url3 = "https://www.apkmirror.com" + match2.group(1) if match2.group(1).startswith("/") else match2.group(1)
    print(f"3-bosqich: To'g'ridan-to'g'ri havola: {url3}")
    
    # Download file
    print("Fayl yuklab olinmoqda...")
    req = urllib.request.Request(url3, headers=headers)
    with urllib.request.urlopen(req) as resp, open(r"C:\Users\MuzaffarZed\ai_workspace\gimbal_tracking.apk", "wb") as f:
        f.write(resp.read())
    print("Yuklab olindi!")
else:
    print("Yuklash tugmasi havolasi:", match2)
    # Print links with 'download'
    for l in re.findall(r'href="([^"]*download[^"]*)"', html2):
        print(" ->", l)
