import asyncio
from bleak import BleakScanner

SERVICE_UUID = '605c8890-d7f7-45d0-a3ba-953f59645e2d' #'605C8890-D7F7-45D0-A3BA-953F59645E2D'

async def main():
    async with BleakScanner() as scanner:
        async for device, advert_data in scanner.advertisement_data():
            if SERVICE_UUID in advert_data.service_uuids:
                print(device)
                break

if __name__ == "__main__":
    asyncio.run(main())

