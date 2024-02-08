import asyncio
from bleak import BleakScanner

# For discovering devicces that exist
async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        
if __name__ == "__main__":
    asyncio.run(main())