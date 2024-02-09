import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = '605c8890-d7f7-45d0-a3ba-953f59645e2d' #'605C8890-D7F7-45D0-A3BA-953F59645E2D'
CHAR_UUID = '4a88f279-f65c-4ecc-8c95-04ac25142a83'

async def main():
    device_c = None
    async with BleakScanner() as scanner:
        async for device, advert_data in scanner.advertisement_data():
            if SERVICE_UUID in advert_data.service_uuids:
                print(device)
                device_c = device.address
                break
    if not device_c:
        print("device not found")
        return
    
    async with BleakClient(device_c) as client:
        for serv in client.services:
            for chars in serv.characteristics:
                print(chars)
        print("Printing char complete")
        char_val = await client.read_gatt_char(CHAR_UUID)
        print(f'Current char value {char_val}')
        
        write_val = bytearray([0x01])
        await client.write_gatt_char(char_specifier=CHAR_UUID, data=write_val)
        
        char_val = await client.read_gatt_char(CHAR_UUID)
        print(f'Current char value {char_val}')
    
    print("After Bleak Client")
    await asyncio.sleep(10.0)

if __name__ == "__main__":
    asyncio.run(main())

