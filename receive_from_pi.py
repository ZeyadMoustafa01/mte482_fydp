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
prev = numpy.zeros(shape=(480, 640, 3), dtype=numpy.uint8)
print('Now waiting for frames...')
start_time = time.time()
while True:
    # First, receive the byte length
    data, address = server.recvfrom(buffSize)
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
    # Receive encoded image data
    data, address = server.recvfrom(buffSize)
    # Perform a simple check
    if length != len(data):
        continue
    # Format conversion
    data = numpy.array(bytearray(data))
    # Decode the image
    imgdecode = cv2.imdecode(data, 1)
    img = cv2.cvtColor(imgdecode, cv2.COLOR_BGR2RGB)
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
    
    # Speed Map
    speed = (depth_map.astype(int) - prev.astype(int)).clip(min=0).astype('uint8')
    prev = depth_map
    
    # Direction from the speed map
    right_side_speed = numpy.mean(speed[:, 480:, :])
    right_center_speed = numpy.mean(speed[:, 320:481, :])
    left_center_speed = numpy.mean(speed[:, 160:321, :])
    left_side_speed = numpy.mean(speed[:, :160, :])
    cv2.imencode
    
    left = left_center_speed + left_side_speed
    right = right_center_speed + right_side_speed
    to_write = 0
    if left > 50 or right > 50:
        if right > left:
            if right_side_speed > right_center_speed:
                print("right\n")
                to_write = 1
            else:
                print("right center\n")
                to_write = 2
        else:
            if left_side_speed > left_center_speed:
                print("left\n")
                to_write = 4
            else:
                print("left center\n")
                to_write = 2
    
    if to_write:
        rpi_server.send(struct.pack('i', to_write))
    
    # FPS
    end_time = time.time()
    fps = 1 / (end_time - start_time)
    start_time = end_time
    
    # Display the frame in a window
    img_out = numpy.hstack((img, depth_map, speed))
    cv2.imshow('frames', img_out)
    
    # Show count and FPS
    count += 1
    print('FPS {}, Write {}, Frames received: {}'.format(round(fps, 3), to_write, count), end='\r')
    
    # Press "ESC" to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break
# Close the socket and window
server.close()
cv2.destroyAllWindows()
print('Destroyed all windows and closed the socket. Exiting...')