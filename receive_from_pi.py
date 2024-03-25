import cv2
import numpy
import socket
import struct
import time
import torch

model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)
midas = torch.hub.load("intel-isl/MiDaS", model_type)

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
# device = torch.device("cpu")
midas.to(device)
midas.eval()

# Load transforms to resize and normalize the image
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

HOST = '192.168.137.1'
PORT = 8000
buffSize = 65535

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the address and port
server.bind((HOST, PORT))

rpi_host = '192.168.137.56' # IP address of the Raspberry Pi - Zeyad
# rpi_host = '192.168.137.28' # IP address of the Raspberry Pi - Akbar
rpi_port = 8001
rpi_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rpi_server.connect((rpi_host, rpi_port))

count = 0
updated_time = 0 
prev = numpy.zeros(shape=(480, 640, 3), dtype=numpy.uint8)
print('Now waiting for frames...')
start_time = time.time()
server.settimeout(5.0)
THERSHOLD = 40
FPS = 9.0
prev_time = time.time()
prev_frames = numpy.zeros(shape=(5, 480, 640, 3), dtype=numpy.uint8)

while True:
    # First, receive the byte length
    
    try:
        data, address = server.recvfrom(buffSize)
    except socket.timeout:
        print('\nNo data received for 5 seconds.\n')
        continue
    # If receiving a close message, stop the program
    if len(data) == 1 and data[0] == 1:
        print('Received close message. Closing the socket and destroying all windows...')
        server.close()
        cv2.destroyAllWindows()
        exit()
    # Perform a simple check; the length value is of type int and takes up four bytes
    if len(data) != 4:
        length = 0
    else:
        length = struct.unpack('i', data)[0]  # Length value
        
    try:
        # Receive encoded image data
        data, address = server.recvfrom(buffSize)
    except socket.timeout:
        print('\nNo data received for 5 seconds. The other one.\n')
        continue
    time_elapsed = time.time() - prev_time
    if time_elapsed > 1.0/FPS:
        prev_time = time.time()
    
        # Perform a simple check
        if length != len(data):
            continue
        # Format conversion
        data = numpy.array(bytearray(data))
        # Decode the image
        f = 1.0
        imgdecode = cv2.imdecode(data, 1)
        img = cv2.cvtColor(imgdecode, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, -1)
        input_batch = transform(img).to(device)
        with torch.no_grad():
            prediction = midas(input_batch)
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        
        output = prediction.cpu().numpy()
        depth_map = cv2.normalize(output, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
        depth_map = (depth_map*255).astype(numpy.uint8)
        depth_map = cv2.applyColorMap(depth_map , cv2.COLORMAP_MAGMA)
        
        # prev_frames = numpy.roll(prev_frames, 1, axis=0)
        # prev_frames[0] = depth_map
        
        # depth_map = numpy.mean(prev_frames, axis=0)
        
        # Speed Map
        speed = (depth_map.astype(int) - prev.astype(int)).clip(min=0).astype('uint8')
        inverse_depth_map = numpy.max(depth_map) - depth_map
        inverse_depth_map = cv2.normalize(inverse_depth_map, None, 0, 3, norm_type=cv2.NORM_MINMAX)
        detectable_speed = numpy.multiply(inverse_depth_map.astype(int), f*speed.astype(int)).clip(min=0).astype(numpy.uint8)
        prev = depth_map
        
        left = numpy.mean(speed[:, :213, :])
        center = numpy.mean(speed[:, 213:426, :])
        right = numpy.mean(speed[:, 426:, :])
        
        if count % 4 == 0:
            left_s = ""+ str(round(left, 3))
            right_s = ""+ str(round(right, 3))
            center_s = ""+ str(round(center, 3))
            
            if left > THERSHOLD:
                left_s = '\033[92m' + left_s + '\033[0m'
            if right > THERSHOLD:
                right_s = '\033[92m' + right_s + '\033[0m'
            if center > THERSHOLD:
                center_s = '\033[92m' + center_s + '\033[0m'
            
            # print(f'Left: {left_s}, Center: {center_s}, Right: {right_s}')
        
        to_write = 0
        dir = numpy.array([right, center, left])
        dir_s = numpy.array(["right", "centre", "left"])
        if numpy.max(dir) > THERSHOLD:
            to_write = numpy.power(2, numpy.argmax(dir))
            print(f"Frame {count}: {dir_s[numpy.argmax(dir)]}")
            
        # if left > THERSHOLD or right > THERSHOLD or center > THERSHOLD:
        #     if right > left:
        #         if right > center:
        #             to_write = 1
        #         else:
        #             to_write = 2
        #     else:
        #         if left > center:
        #             to_write = 4
        #         else:
        #             to_write = 2
        
        # Direction from the speed map
        # right_side_speed = numpy.mean(detectable_speed[:, 480:, :])
        # right_center_speed = numpy.mean(detectable_speed[:, 320:481, :])
        # left_center_speed = numpy.mean(detectable_speed[:, 160:321, :])
        # left_side_speed = numpy.mean(detectable_speed[:, :160, :])
        
        # left = left_center_speed + left_side_speed
        # right = right_center_speed + right_side_speed
        # to_write = 0
        # if left > 70 or right > 70:
        #     if right > left:
        #         if right_side_speed > right_center_speed:
        #             print("right\n")
        #             to_write = 1
        #         else:
        #             print("right center\n")
        #             to_write = 2
        #     else:
        #         if left_side_speed > left_center_speed:
        #             print("left\n")
        #             to_write = 4
        #         else:
        #             print("left center\n")
        #             to_write = 2
        
        if to_write and time.time() - updated_time > 2:
            rpi_server.send(struct.pack('i', to_write))
            updated_time = time.time()
        
        # FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)
        start_time = end_time
        
        # Display the frame in a window
        img_out = numpy.hstack((img, depth_map))
        img_out = numpy.vstack((img_out, numpy.hstack((speed, detectable_speed))))
        cv2.imshow('frames', img_out)
        
        # Show count and FPS
        count += 1
        # print('FPS {}, Write {}, Frames received: {}'.format(round(fps, 3), to_write, count), end='\r')
        
        # Press "ESC" to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break
# Close the socket and window
server.close()
cv2.destroyAllWindows()
print('Destroyed all windows and closed the socket. Exiting...')