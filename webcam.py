import cv2
import numpy as np
import signal
from ble_class import BleComm
import asyncio
import sys
import random
import time

async def main():
    camera = cv2.VideoCapture(0)
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

    # def handler(signum, frame):
    #     camera.release()
    #     cv2.destroyAllWindows()
    #     print("PROGRAM STOPPED!")
    #     sys.exit()

    # signal.signal(signal.SIGINT, handler)
    rng = np.random.default_rng()
    ble_comm = BleComm()
    await ble_comm.get_device()
    
    while True:
        # Read frame from webcam
        ret, img = camera.read()
        
        if ret:
            rand = random.randint(0, 3)
            # print(f"Rand {rand}, {rand.to_bytes()}")
            
            print(f"Start: {time.strftime('%X')}")
            await ble_comm.write_ble(rand)
            print(f"End: {time.strftime('%X')}")
            
        if cv2.waitKey(1) == ord("q"):
            break
            
    camera.release()
    cv2.destroyAllWindows()
    print("PROGRAM STOPPED")

if __name__ == "__main__":
    asyncio.run(main=main())
