import cv2
import numpy as np
from MidasDepthEstimation.midasDepthEstimator import midasDepthEstimator
import time

# Initialize depth estimation model
depthEstimator = midasDepthEstimator()

# Initialize webcam
camera = cv2.VideoCapture(0)
cv2.namedWindow("Depth Image", cv2.WINDOW_NORMAL)

while True:
    # Read frame from the webcam
    ret, img = camera.read()
    start = time.time()

    # Estimate depth
    colorDepth = depthEstimator.estimateDepth(img)

    # Add the depth image over the color image:
    combinedImg = cv2.addWeighted(img, 0.7, colorDepth, 0.6, 0)

    # Join the input image, the estiamted depth and the combined image
    img_out = np.hstack((img, colorDepth))  # , combinedImg))
    end = time.time()
    totalTime = end - start
    fps = 1 / totalTime
    # print(round(fps, 3))
    cv2.putText(img_out, f"FPS: {int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    cv2.imshow("Depth Image", img_out)

    # cv2.imshow("Color Image", img)
    # print(round(fps, 3))

    # Press key q to stop
    if cv2.waitKey(1) == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
