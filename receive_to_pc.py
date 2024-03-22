import socket
import struct
import asyncio

async def receive_dir(queue: asyncio.Queue):
    HOST = '192.168.137.56'
    PORT = 8001
    buffsize = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.setblocking(False)

    loop = asyncio.get_running_loop()
    
    while True:
        try:
            client_socket, address = await loop.sock_accept(server)
            client_socket.setblocking(False)
            while True:
                data = await loop.sock_recv(client_socket, buffsize)
                
                val = struct.unpack('i', data)[0]
                await queue.put(val)
                print(f'\nData Received: {val}\n')
        except Exception as e:
            print('Receiving stopped...')
            client_socket.close()
        except KeyboardInterrupt as e:
            print('Keyboard interrupt ', e)
            client_socket.close()
            server.close()