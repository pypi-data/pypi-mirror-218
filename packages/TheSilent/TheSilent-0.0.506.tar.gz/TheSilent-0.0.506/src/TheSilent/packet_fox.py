import binascii
import socket
from TheSilent.clear import clear

CYAN = "\033[1;36m"

def packet_fox():
    clear()
    interfaces = socket.if_nameindex()
    sniffer_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    for interface in interfaces:
        if interface[1] != "lo":
            try:
                sniffer_socket.bind((interface[1],interface[0]))
                print(CYAN + f"listening on interface:{interface[1]} port:{interface[0]}")

            except OSError:
                continue

    while True:
        try:
            packet = sniffer_socket.recv(65536)
            data = binascii.hexlify(packet).decode()
            with open("hex_dump.txt", "a") as file:
                file.write(data + "\n")

        except OSError:
            pass

packet_fox()
