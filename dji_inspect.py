import asyncio
import sys
from bleak import BleakClient

# UTF-8 console support for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ADDRESS = "CA:41:0A:00:E9:B6"

async def inspect():
    print(f"DJI Osmo Mobile ({ADDRESS}) ga ulanmoqda...")
    async with BleakClient(ADDRESS, timeout=12.0) as client:
        connected = client.is_connected
        print(f"Ulanish holati: {'Muvaffaqiyatli!' if connected else 'Ulanmadi'}")
        
        if not connected:
            return

        print("\n--- Mavjud GATT Xizmatlari va Xarakteristikalari ---")
        for service in client.services:
            print(f"\n[Xizmat]: {service.description} ({service.uuid})")
            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"  |-- [Xarakteristika]: {char.description} ({char.uuid}) | Xususiyatlar: [{props}]")

if __name__ == "__main__":
    asyncio.run(inspect())
