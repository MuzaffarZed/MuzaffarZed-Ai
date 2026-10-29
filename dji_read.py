import asyncio
import sys
from bleak import BleakClient

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ADDRESS = "CA:41:0A:00:E9:B6"

# Standard UUIDs
BATTERY_CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
MFR_NAME_CHAR_UUID = "00002a29-0000-1000-8000-00805f9b34fb"
DEV_NAME_CHAR_UUID = "00002a00-0000-1000-8000-00805f9b34fb"

async def read_telemetry():
    print(f"DJI Osmo Mobile ({ADDRESS}) ga ulanmoqda...")
    async with BleakClient(ADDRESS, timeout=12.0) as client:
        if not client.is_connected:
            print("Ulanib bo'lmadi!")
            return

        print("Ulanish muvaffaqiyatli!\n")

        # 1. Device Name
        try:
            dev_name = await client.read_gatt_char(DEV_NAME_CHAR_UUID)
            print(f"1. Qurilma nomi: {dev_name.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"Qurilma nomini o'qishda xato: {e}")

        # 2. Manufacturer
        try:
            mfr = await client.read_gatt_char(MFR_NAME_CHAR_UUID)
            print(f"2. Ishlab chiqaruvchi: {mfr.decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"Ishlab chiqaruvchini o'qishda xato: {e}")

        # 3. Battery Level
        try:
            battery = await client.read_gatt_char(BATTERY_CHAR_UUID)
            print(f"3. Batareya zaryadi: {battery[0]}%")
        except Exception as e:
            print(f"Batareyani o'qishda xato: {e}")

if __name__ == "__main__":
    asyncio.run(read_telemetry())
