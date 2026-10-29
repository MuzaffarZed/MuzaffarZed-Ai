import asyncio
import sys
from bleak import BleakClient

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ADDRESS = "CA:41:0A:00:E9:B6"
NOTIFY_UUID_1 = "0000fff4-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID_2 = "15f1e603-a277-43fc-a484-dd39ef8a9100"

def callback_fff4(sender, data: bytearray):
    print(f"[FFF4 Telemetriya]: {data.hex(' ')}")

def callback_15f1(sender, data: bytearray):
    print(f"[15F1 Voqea]: {data.hex(' ')}")

async def listen():
    print(f"DJI Osmo Mobile ({ADDRESS}) ga ulanmoqda...")
    async with BleakClient(ADDRESS, timeout=12.0) as client:
        print("Ulandi! Tugmalar va joystik signallari tinglanmoqda...")
        
        try:
            await client.start_notify(NOTIFY_UUID_1, callback_fff4)
            print(f"FFF4 kanaliga ulandi.")
        except Exception as e:
            print(f"FFF4 ulanmadi: {e}")

        try:
            await client.start_notify(NOTIFY_UUID_2, callback_15f1)
            print(f"15F1 kanaliga ulandi.")
        except Exception as e:
            print(f"15F1 ulanmadi: {e}")

        print("\n>>> Endi gimbaldagi tugmalarni yoki joystikni bosing/harakatlantiring (10 soniya)...")
        await asyncio.sleep(10.0)
        
        await client.stop_notify(NOTIFY_UUID_1)
        await client.stop_notify(NOTIFY_UUID_2)
        print("\nTinglash yakunlandi.")

if __name__ == "__main__":
    asyncio.run(listen())
