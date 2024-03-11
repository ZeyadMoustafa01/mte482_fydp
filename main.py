from BLE.ble_class import BleComm
from webcamDepthEstimation import depth
import asyncio

async def main():
    queue = asyncio.Queue()
    ble_comm = BleComm()
    await ble_comm.get_device()
    await asyncio.gather(depth(queue), ble_comm.write_ble(queue))
    

if __name__ == "__main__":
    asyncio.run(main())