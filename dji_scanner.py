import asyncio
from bleak import BleakScanner

async def scan():
    print("Skanerlash boshlandi... Yaqin atrofdagi BLE qurilmalar qidirilmoqda (7 soniya)...")
    devices = await BleakScanner.discover(timeout=7.0, return_adv=True)
    
    found = []
    for address, (device, adv) in devices.items():
        name = device.name or adv.local_name or "Noma'lum"
        rssi = adv.rssi
        found.append((name, address, rssi, adv.service_uuids))
        
    print(f"\nJami topilgan qurilmalar: {len(found)}")
    print("-" * 65)
    print(f"{'Qurilma nomi':<30} | {'MAC Manzili':<18} | {'Signal (RSSI)':<10}")
    print("-" * 65)
    
    dji_candidates = []
    for name, address, rssi, uuids in sorted(found, key=lambda x: x[2], reverse=True):
        print(f"{name:<30} | {address:<18} | {rssi:<10}")
        if any(keyword in name.upper() for keyword in ["DJI", "OSMO", "OM", "GIMBAL"]):
            dji_candidates.append((name, address, rssi, uuids))
            
    print("-" * 65)
    if dji_candidates:
        print("\n>>> DJI qurilmalari topildi:")
        for name, address, rssi, uuids in dji_candidates:
            print(f" -> Nomi: {name}, Manzili: {address}, Signal kuchi: {rssi} dBm")
    else:
        print("\n>>> Maxsus 'DJI' nomli qurilma nomi to'g'ridan-to'g'ri ko'rinmadi.")
        print("Yuqoridagi ro'yxatda noma'lum yoki boshqa nom bilan ko'ringan bo'lishi mumkin.")

if __name__ == "__main__":
    asyncio.run(scan())
