import binascii
import os
import socket
import sys
from sys import platform
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"

def beacon_swat(interface):
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

        ssid_list = []
        beacon_list = []
        
        print(CYAN + "scanning for networks\n")
        while True:
            try:
                packet = my_socket.recv(65536)
                data = binascii.hexlify(packet).decode()

                if data[0:8] == "00001800" and  data[48:50] == "80":
                    ssid_length = int(data[121:124], 16)
                    ssid = bytearray.fromhex(data[124:124+ssid_length*2]).decode()
                    add = True
                    for name in ssid_list:
                        if name == ssid:
                            add = False

                    if add:
                        print("found: " + ssid)
                        ssid_list.append(ssid)
                        with open("ssid_list.txt", "a") as file:
                            file.write(ssid + "\n")
                        with open("beacons.txt", "a") as file:
                            file.write(data + "\n")

            except OSError:
                os.system(f"sudo ip link set {interface} down")
                os.system(f"sudo iw {interface} set monitor control")
                os.system(f"sudo ip link set {interface} up")
                continue

    except PermissionError:
        print(RED + "ERROR! Permission Denied!")
        sys.exit()
