import asyncio
from ble_class import BleComm

async def main(loop, ble_comm: BleComm, to_write) -> None:
    for _ in range(5):
        if not ble_comm.device_found():
            await ble_comm.get_device()
            await asyncio.sleep(5.0)
        
        await ble_comm.write(to_write.to_bytes())
        
        to_write = (to_write + 1) % 8
        await asyncio.sleep(5.0)
        
    await ble_comm.disconnect()
        
    

if __name__ == "__main__":
    ble_comm = BleComm()
    loop = asyncio.get_event_loop()
    to_write: int = 1
    
    loop.run_until_complete(main(loop,  ble_comm, to_write))
    loop.close()
    