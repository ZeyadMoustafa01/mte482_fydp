import asyncio
from bleak import BleakScanner, BleakClient

SERVICE_UUID = '605c8890-d7f7-45d0-a3ba-953f59645e2d'
CHAR_UUID = '4a88f279-f65c-4ecc-8c95-04ac25142a83'

class BleComm:
    def __init__():
        device = None
        client = None
        
    async def get_device(self):
        async with BleakScanner() as scanner:
            async for device, advert_data in scanner.advertisement_data():
                if SERVICE_UUID in advert_data.service_uuids:
                    print(device)
                    self.device = device.address
                    break
    
    def disconnected(self, client: BleakClient):
        pass
        
    async def connect(self) -> bool:
        try:
            self.client = BleakClient(address_or_ble_device=self.device,
                                      disconnected_callback=self.disconnected)
            return True
        except:
            print("Unable to connect")
            return False
        
    def check_con(self):
        return not self.client or not self.client.is_connected
    
    async def write(self, val: bytearray):
        if len(bytearray) > 8 or not len(bytearray):
            print("Bytearray size incorrect.")
            return
        
        if not self.check_con():
            if not self.connect():
                print("Device not connected.")
                return

        curr_val = await client.read_gatt_char()