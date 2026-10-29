import asyncio
import sys
from bleak import BleakClient

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ADDRESS = "CA:41:0A:00:E9:B6"
CHAR_FFF4 = "0000fff4-0000-1000-8000-00805f9b34fb"
CHAR_FFF5 = "0000fff5-0000-1000-8000-00805f9b34fb"

def on_notify_fff4(sender, data: bytearray):
    print(f"[FFF4 Xabar ({len(data)} bayt)]: {data.hex(' ')}")

def on_notify_fff5(sender, data: bytearray):
    print(f"[FFF5 Xabar ({len(data)} bayt)]: {data.hex(' ')}")

async def pair_test():
    print(f"DJI Osmo Mobile ({ADDRESS}) ga ulanmoqda...")
    async with BleakClient(ADDRESS, timeout=12.0) as client:
        print("Ulandi! Xabarlar tinglanmoqda...")
        await client.start_notify(CHAR_FFF4, on_notify_fff4)
        
        try:
            await client.start_notify(CHAR_FFF5, on_notify_fff5)
        except Exception:
            pass

        print("Juftlash (pairing) signali [0x01, 0x00] fff4 ga yuborilmoqda...")
        try:
            await client.write_gatt_char(CHAR_FFF4, bytearray([0x01, 0x00]), response=True)
            print("fff4 ga yozildi!")
        except Exception as e:
            print(f"fff4 ga yozishda xato: {e}")
            try:
                await client.write_gatt_char(CHAR_FFF4, bytearray([0x01, 0x00]), response=False)
                print("fff4 ga response=False bilan yozildi!")
            except Exception as e2:
                print(f"Ikkala usulda ham xato: {e2}")

        print("\nKuzatilmoqda (5 soniya)...")
        await asyncio.sleep(5.0)

        await client.stop_notify(CHAR_FFF4)

if __name__ == "__main__":
    asyncio.run(pair_test())
