import binascii
import socket

CYAN = "\033[1;36m"

def packet_fox():
    interfaces = socket.if_nameindex()
    sniffer_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    for interface in interfaces:
        if interface[1] != "lo":
            print(CYAN + f"listening on interface:{interface[1]} port:{interface[0]}")
            sniffer_socket.bind((interface[1],interface[0]))

    while True:
        packet = sniffer_socket.recv(65536)
        data = binascii.hexlify(packet).decode()
        with open("hex_dump.txt", "a") as file:
            file.write(data + "\n")

packet_fox()
