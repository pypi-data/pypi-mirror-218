import binascii
import os
import psutil
import random
import socket
import sys
import threading
import time
from sys import platform
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"

def probe_request(interface):
    hex_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    mac = "7cc180"
    for _ in range(6):
        mac += hex_characters[random.randint(0,15)]
        
    probe_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    probe_socket.bind((interface, 1))
    my_code = binascii.unhexlify("000018002e4000a02008000000026c09a000bd000000bd0040000000ffffffffffff" + mac.lower() + mac.lower() + "00019f01770a4f0100006400010400" + "06" + "ffffffffffff" + "010882848b962430486c0301010504000100002a01002f010032040c121860dd090010180200f02c0000dd180050f2020101800003a4000027a4000042435e0062022f00")
    while True:
        try:
            time.sleep(15)
            probe_socket.sendall(my_code)

        except OSError:
            os.system(f"sudo ip link set {interface} down")
            os.system(f"sudo iw {interface} set monitor control")
            os.system(f"sudo ip link set {interface} up")
            continue

def beacon_thief():
    clear()
    interface_list = psutil.net_if_addrs()
    for interfaces in interface_list.keys():
        interface = interfaces

    my_thread = threading.Thread(target=probe_request, args=[interface]).start()

    try:
        if platform != "linux":
            print(RED + "Unsupported platform! Linux is required for this tool!")
            sys.exit()
            

        my_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        my_socket.bind((interface, 0))

        ssid_list = []
        beacon_list = []

        if os.path.exists("ssid_list.txt"):
            with open("ssid_list.txt", "r") as file:
                for f in file:
                    f = f.replace("\n", "")
                    print(CYAN + f)
                    ssid_list.append(f)

        while True:
            try:
                packet = my_socket.recv(65536)
                data = binascii.hexlify(packet).decode()

                if data[0:8] == "00001800" and  data[48:50] == "80" or data[0:8] == "00001800" and  data[48:50] == "50":
                    ssid_length = int(data[121:124], 16)
                    ssid = bytearray.fromhex(data[124:124+ssid_length*2]).decode()
                    add = True
                    for name in ssid_list:
                        if name == ssid:
                            add = False
                            break

                    if add:
                        print(CYAN + ssid)
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
