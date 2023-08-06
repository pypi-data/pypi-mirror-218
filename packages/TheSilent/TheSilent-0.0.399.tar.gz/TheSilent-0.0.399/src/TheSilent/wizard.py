from TheSilent.ap import *
from TheSilent.arp_void import *
from TheSilent.beacon_thief import *
from TheSilent.brute_force_hash import *
from TheSilent.clear import *
from TheSilent.dictionary_hash import *
from TheSilent.hex_viewer import *
from TheSilent.osint import *
from TheSilent.packet_sniffer import *
from TheSilent.secure_overwrite import *
from TheSilent.source_code_viewer import *
from TheSilent.web_scanner import *

CYAN = "\033[1;36m"

def main():
    print(CYAN + "")
    clear()

    print("1 | rogue access point | linux/root/monitor mode")
    print("2 | arp flooding dos attack | linux/root")
    print("3 | beacon thief | linux/root/monitor mode")
    print("4 | brute force hash | all")
    print("5 | dictionary force hash | all")
    print("6 | hex viewer | all")
    print("7 | osint | all")
    print("8 | packet sniffer | linux/root")
    print("9 | secure overwrite | all/root may be required")
    print("10 | source code viewer | all")
    print("11 | web scanner | all")
    print("")
    tool = input()

    if tool == "1":
        clear()
        name = input("name\n")
        interface = input("interface\n")
        ap(name, interface)

    if tool == "2":
        clear()
        router = input("ip of router\n")
        interface = input("interface\n")
        arp_void(router, interface)

    if tool == "3":
        clear()
        interface = input("interface\n")
        beacon_thief(interface)

    if tool == "4":
        clear()
        my_hash = input("hash\n")
        brute_force_hash(my_hash)

    if tool == "5":
        clear()
        my_file = input("file\n")
        my_hash = input("hash\n")
        dictionary_hash(my_file, my_hash, mask=True)

    if tool == "6":
        clear()
        file = input("file\n")
        hex_viewer(file)

    if tool == "7":
        clear()
        username = input("username\n")
        print(username)

    if tool == "8":
        clear()
        packet_sniffer(data=True, hex_dump=True)

    if tool == "9":
        clear()
        device = input("file, folder, or device\n")
        secure_overwrite(device)

    if tool == "10":
        clear()
        file = input("file\n")
        source_code_viewer(file)

    if tool == "11":
        clear()
        host = input("host\n")
        print(web_scanner(host))

main()
