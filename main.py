from BLE.ble_class import BleComm
from send_to_pc import send_stream
from receive_to_pc import receive_dir
import asyncio

async def main():
    queue = asyncio.Queue()
    ble_comm = BleComm()
    await ble_comm.get_device()
    await asyncio.gather(send_stream(), receive_dir(queue), ble_comm.write_ble(queue))
    
    # Uncomment if testing without Arduino
    # await asyncio.gather(send_stream(), receive_dir(queue))

if __name__ == '__main__':
    asyncio.run(main())