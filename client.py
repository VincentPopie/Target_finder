# Vincent Popie

import socket
import struct


class Client:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def mysend(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent += sent

    def myreceive(self):
        # data lenth is packed into 4 bytes

        chunks = []
        bytes_recd = 0
        SIZE_DATA_LENGTH = 4

        while bytes_recd < SIZE_DATA_LENGTH:
            chunk = self.sock.recv((SIZE_DATA_LENGTH, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)

        MSGLEN = struct.unpack('>I', chunks[:SIZE_DATA_LENGTH])[0]

        bytes_recd -= SIZE_DATA_LENGTH
        chunks = chunks[SIZE_DATA_LENGTH:]

        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)
