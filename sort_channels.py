import subprocess, time, sys

sys.stdout.reconfigure(encoding='utf-8')
adb = r'C:\Users\MuzaffarZed\AppData\Local\Microsoft\WinGet\Packages\Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe\platform-tools\adb.exe'

def key(k):
    subprocess.run([adb, 'shell', f'input keyevent {k}'])
    time.sleep(0.2)

def jump_to(num):
    key(185) # YELLOW
    time.sleep(0.25)
    subprocess.run([adb, 'shell', f'input text {num}'])
    time.sleep(0.15)
    key(66) # ENTER focuses OK
    time.sleep(0.15)
    key(23) # DPAD_CENTER clicks OK
    time.sleep(0.3)

def swap(a, b):
    print(f'Swapping pos {a} <-> pos {b}...')
    jump_to(a)
    key(23) # Select A
    time.sleep(0.25)
    jump_to(b)
    key(23) # Confirm swap
    time.sleep(0.4)

def read_all_channels():
    # Scroll to top first
    key(183)
    key(183)
    time.sleep(0.3)
    channels = {}
    for _ in range(3):
        subprocess.run([adb, 'shell', 'uiautomator dump /sdcard/page.xml'], capture_output=True)
        res = subprocess.run([adb, 'shell', 'cat /sdcard/page.xml'], capture_output=True, encoding='utf-8', errors='ignore')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res.stdout)
        nums = []
        names = []
        for n in root.iter('node'):
            t = n.attrib.get('text', '')
            b = n.attrib.get('bounds', '')
            if t.isdigit() and '[832,' in b:
                nums.append(int(t))
            elif t and not t.isdigit() and '[888,' in b:
                names.append(t)
        for u, m in zip(nums, names):
            channels[u] = m
        key(184) # Pastga varaqlash
        time.sleep(0.3)
    # Scroll back to top
    key(183)
    key(183)
    time.sleep(0.2)
    return channels

target_order = [
    'O`zbekiston',
    'Yoshlar',
    'Toshkent',
    'Sport',
    'Madaniyat va ma`rifat',
    'Dunyo  bo`ylab',
    'Bolajon',
    'Navo',
    'Mahalla',
    'Kinoteatr',
    'O`zbekiston 24',
    'O`zbekiston tarixi',
    'Milliy TV',
    'Sevimli TV',
    'ZO`R TV',
    'MY5',
    'UzReport',
    'Futbol TV',
    'AQLVOY',
    'Renessans TV',
    'FTV',
    'Nurafshon'
]

def main():
    print('Reading initial channel state...')
    current = read_all_channels()
    print('Initial channels count:', len(current))

    for target_idx, desired_name in enumerate(target_order, 1):
        # Refresh position of desired_name
        current_pos = None
        for p, name in current.items():
            if name == desired_name:
                current_pos = p
                break
        
        if current_pos is None:
            print(f'Warning: {desired_name} not found in channels!')
            continue
            
        if current_pos != target_idx:
            swap(target_idx, current_pos)
            # Update local current dict
            old_name_at_target = current[target_idx]
            current[target_idx] = desired_name
            current[current_pos] = old_name_at_target
            print(f'Now pos {target_idx} is {desired_name}')

    print('Finished all swaps! Verifying final channel list...')
    final_channels = read_all_channels()
    print('=== FINAL ORDERED CHANNELS ===')
    for num in sorted(final_channels.keys()):
        print(f'{num}: {final_channels[num]}')

if __name__ == '__main__':
    main()
