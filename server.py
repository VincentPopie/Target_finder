# Vincent Popie

import socket
import struct

class Server:

    def __init__(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_launch = False
        self.connected_client = []

    def launch(self, port):
        self.serversock.bind((socket.gethostbyname(socket.gethostname()), port))
        self.serversock.listen(5)
        self.server_launch = True

    def mysend(self, msg, client):
        msg = struct.pack('>I', len(msg)) + msg
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = client.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent += sent

    def myreceive(self, client):
        # data lenth is packed into 4 bytes
        chunks = []
        bytes_recd = 0
        SIZE_DATA_LENGTH = 4

        while bytes_recd < SIZE_DATA_LENGTH:
            chunk = client.recv(min(SIZE_DATA_LENGTH, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)

        data = b''.join(chunks[:SIZE_DATA_LENGTH])
        MSGLEN = struct.unpack('>I', data)[0]

        bytes_recd -= SIZE_DATA_LENGTH
        chunks = chunks[SIZE_DATA_LENGTH:]

        while bytes_recd < MSGLEN:
            chunk = self.serversock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)



