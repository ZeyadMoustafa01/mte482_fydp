import cv2
import numpy as np
import signal
from ble_class import BleComm
import asyncio
import sys
import random
import time

async def read_cam(queue: asyncio.Queue):
    # camera = cv2.VideoCapture(0)
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

    # def handler(signum, frame):
    #     camera.release()
    #     cv2.destroyAllWindows()
    #     print("PROGRAM STOPPED!")
    #     sys.exit()

    # signal.signal(signal.SIGINT, handler)
    rng = np.random.default_rng()
    count = 0
    while True:
        # Read frame from webcam
        # ret, img = camera.read()
        ret = True
        if ret:
            rand = random.randint(0, 3)
            # print(f"Rand {rand}, {rand.to_bytes()}")
            
            print(f"Start: {time.strftime('%X')}")
            # write_task = asyncio.create_task(ble_comm.write_ble(rand))
            if queue.qsize() > 0:
                queue._queue.clear()
                count += 1
                print(f"Cleared {count}")
            await queue.put(rand)
            await asyncio.sleep(0.05)
            
            
        if cv2.waitKey(1) == ord("q"):
            break
            
    # camera.release()
    cv2.destroyAllWindows()
    print("PROGRAM STOPPED")

async def main():
    queue = asyncio.Queue()
    ble_comm = BleComm()
    await ble_comm.get_device()
    await asyncio.gather(read_cam(queue), ble_comm.write_ble(queue))
    

if __name__ == "__main__":
    asyncio.run(main())
    
