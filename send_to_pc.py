import cv2
import numpy
import socket
import struct
import asyncio

async def send_stream():
    HOST = '192.168.137.1'
    PORT = 8000
    
    # Create a UDP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.connect((HOST, PORT))  # Connect to the target address
    server.setblocking(False)
    print('Now starting to send frames...')
    
    loop = asyncio.get_running_loop()
    
    # Get the camera device
    capture = cv2.VideoCapture(0)
    count = 0
    
    try:
        while True:
            success, frame = capture.read()
            while not success and frame is None:
                success, frame = capture.read()  # Get a video frame
            # Encode the image
            result, imgencode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])

            # Send the byte length of the encoded image data
            await loop.sock_sendall(server, struct.pack('i', len(imgencode.tobytes())))
            # Send the video frame data
            await loop.sock_sendall(server, imgencode)
            
            count += 1
            print(f'Sending frame {count}', end='\r')
            await asyncio.sleep(0.1) # Try changing this maybe(?)
    except Exception as e:
        print(e)
        # Send a close message
        server.sendall(struct.pack('B', 1))
        # Release camera resources
        capture.release()
        # Close the socket
        server.close()
        print('Sending stopped...')