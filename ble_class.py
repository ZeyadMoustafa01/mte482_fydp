import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

SERVICE_UUID = '605c8890-d7f7-45d0-a3ba-953f59645e2d'
CHAR_UUID = '4a88f279-f65c-4ecc-8c95-04ac25142a83'

class BleComm:
    def __init__(self):
        self.device = None
        self.client = None
        self.scanner = BleakScanner(detection_callback=self.detection_callback,
                                    service_uuids=[SERVICE_UUID])
        
    def device_found(self):
        return self.device
    
    def detection_callback(self, device: BLEDevice, advert_data: AdvertisementData) -> None:
        print(f"Device found: {device}")
        self.device = device.address
        asyncio.create_task(self.scanner.stop())
        asyncio.create_task(self.connect())
    
    async def get_device(self) -> None:
        print("Searching for device")
        await self.scanner.start()
        await asyncio.sleep(5.0)
        await self.scanner.stop()
    
    def disconnected(self, client: BleakClient) -> None:
        print("Device has been disconnected")
        pass
        
    async def connect(self) -> bool:
        try:
            self.client = BleakClient(address_or_ble_device=self.device,
                                      disconnected_callback=self.disconnected)
            await self.client.connect()
            print(f"Connected to device {self.device}")
            return True
        except:
            print("Unable to connect")
            return False
    
    async def disconnect(self) -> None:
        await self.client.disconnect()
        
    def check_con(self) -> bool:
        return self.client and self.client.is_connected
    
    async def write(self, val: bytearray) -> None:
        if len(val) > 3 or not len(val):
            print("Bytearray size incorrect.")
            return
        
        if not self.check_con():
            if not self.connect():
                print("Unable to connect to device")
                return

        curr_val = await self.client.read_gatt_char(CHAR_UUID)
        print(f"The current CHAR value is {curr_val}")
        
        await self.client.write_gatt_char(char_specifier=CHAR_UUID, data=val)
        
        new_val = await self.client.read_gatt_char(CHAR_UUID)
        print(f"The new char value is: {new_val}")