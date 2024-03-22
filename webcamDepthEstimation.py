import cv2
import numpy as np
from MidasDepthEstimation.midasDepthEstimator import midasDepthEstimator
import time
import asyncio

async def depth(queue: asyncio.Queue):
    # Initialize depth estimation model
    depthEstimator = midasDepthEstimator()
    FPS = 1.2

    # Initialize webcam
    camera = cv2.VideoCapture(0)
    # cv2.namedWindow("Depth Image", cv2.WINDOW_NORMAL)
    prev = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
    prev_time = time.time()
    while True:
        time_elasped = time.time() - prev_time
        ret, img = camera.read()
        # Read frame from the webcam
        if time_elasped > 1.0/FPS:
            prev_time = time.time()
            
            start = time.time()
            img = cv2.flip(img, -1)

            # Estimate depth
            colorDepth = depthEstimator.estimateDepth(img)
            # print(colorDepth.shape)

            # Add the depth image over the color image:
            # combinedImg = cv2.addWeighted(img, 0.7, colorDepth, 0.6, 0)

            # Join the input image, the estiamted depth and the combined image
            speed = (colorDepth.astype(int) - prev.astype(int)).clip(min=0).astype('uint8')
            prev = colorDepth
            img_out = np.hstack((img, colorDepth, speed))  # , combinedImg))
            end = time.time()
            totalTime = end - start
            fps = 1 / totalTime
            # print(round(fps, 3))
            
            right_side_speed = np.mean(speed[:, 480:, :])
            right_center_speed = np.mean(speed[:, 320:481, :])
            left_center_speed = np.mean(speed[:, 160:321, :])
            left_side_speed = np.mean(speed[:, :160, :])

            # cv2.putText(img_out, f"FPS: {round(fps, 3)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            # cv2.imshow("Depth Image", img_out)
            
            
            left = left_center_speed + left_side_speed
            right = right_center_speed + right_side_speed
            to_write = 0
            if left > 50 or right > 50:
                if right > left:
                    if right_side_speed > right_center_speed:
                        print("right")
                        to_write = 1
                    else:
                        print("right center")
                        to_write = 2
                else:
                    if left_side_speed > left_center_speed:
                        print("left")
                        to_write = 4
                    else:
                        print("left center")
                        to_write = 2
            if to_write:
                if queue.qsize() > 0:
                    queue._queue.clear()
                    
                await queue.put(to_write)
                await asyncio.sleep(0.5)
            

            # Press key q to stop
            if cv2.waitKey(1) == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()
