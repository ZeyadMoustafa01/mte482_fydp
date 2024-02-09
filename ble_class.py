import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

SERVICE_UUID = '605c8890-d7f7-45d0-a3ba-953f59645e2d'
CHAR_UUID = '4a88f279-f65c-4ecc-8c95-04ac25142a83'

class BleComm:
    def __init__(self):
        self.__device = None
        self.__client = None
        self.__scanner = BleakScanner(detection_callback=self.__detection_callback,
                                    service_uuids=[SERVICE_UUID])
        
    def device_found(self):
        return self.__device != None
    
    def __detection_callback(self, device: BLEDevice, advert_data: AdvertisementData) -> None:
        print(f"Device found: {device}")
        self.__device = device.address
        asyncio.create_task(self.__scanner.stop())
        asyncio.create_task(self.connect())
    
    async def get_device(self) -> None:
        print("Searching for device")
        await self.__scanner.start()
        await asyncio.sleep(5.0)
        await self.__scanner.stop()
    
    def __client_disconnected(self, client: BleakClient) -> None:
        print("Device has been disconnected")
        pass
        
    async def connect(self) -> bool:
        try:
            self.__client = BleakClient(address_or_ble_device=self.__device,
                                      disconnected_callback=self.__client_disconnected)
            await self.__client.connect()
            print(f"Connected to device {self.__device}")
            return True
        except:
            print("Unable to connect")
            return False
    
    async def disconnect(self) -> None:
        await self.__client.disconnect()
        
    def check_con(self) -> bool:
        return self.__client and self.__client.is_connected
    
    async def write(self, val: bytearray) -> None:
        if len(val) > 3 or not len(val):
            print("Bytearray size incorrect.")
            return
        
        if not self.check_con():
            if not await self.connect():
                print("Unable to connect to device")
                return

        curr_val = await self.__client.read_gatt_char(CHAR_UUID)
        print(f"The current CHAR value is {curr_val}")
        
        await self.__client.write_gatt_char(char_specifier=CHAR_UUID, data=val)
        
        new_val = await self.__client.read_gatt_char(CHAR_UUID)
        print(f"The new char value is: {new_val}")