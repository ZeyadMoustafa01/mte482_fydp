import cv2
import numpy as np
from MidasDepthEstimation.midasDepthEstimator import midasDepthEstimator
import time

# Initialize depth estimation model
depthEstimator = midasDepthEstimator()
FPS = 1.2

# Initialize webcam
camera = cv2.VideoCapture(0)
cv2.namedWindow("Depth Image", cv2.WINDOW_NORMAL)
prev = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
prev_time = time.time()
while True:
    time_elasped = time.time() - prev_time
    ret, img = camera.read()
    # Read frame from the webcam
    if time_elasped > 1.0/FPS:
        prev_time = time.time()
        
        start = time.time()

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
        
        right_side_speed = np.sum(np.mean(speed[:, 480:, :], axis=(0, 1)))
        right_center_speed = np.sum(np.mean(speed[:, 320:481, :], axis=(0, 1)))
        left_center_speed = np.sum(np.mean(speed[:, 160:321, :], axis=(0, 1)))
        left_side_speed = np.sum(np.mean(speed[:, :160, :], axis=(0, 1)))

        cv2.putText(img_out, f"FPS: {round(fps, 3)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        cv2.imshow("Depth Image", img_out)
        
        
        left = left_center_speed + left_side_speed
        right = right_center_speed + right_side_speed
        if left > 85 or right > 85:
            if right > left:
                if right_side_speed > right_center_speed:
                    print("right")
                else:
                    print("right center")
            else:
                if left_side_speed > left_center_speed:
                    print("left")
                else:
                    print("left center")
        
        

        # Press key q to stop
        if cv2.waitKey(1) == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()
