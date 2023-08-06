from TheSilent.ap import *
from TheSilent.arp_void import *
from TheSilent.beacon_swarm import *
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
    print("3 | beacon swarm | linux/root/monitor mode")
    print("4 | beacon thief | linux/root/monitor mode")
    print("5 | brute force hash | all")
    print("6 | dictionary force hash | all")
    print("7 | hex viewer | all")
    print("8 | osint | all")
    print("9 | packet sniffer | linux/root")
    print("10 | secure overwrite | all/root may be required")
    print("11 | source code viewer | all")
    print("12 | web scanner | all")
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
        beacon_swarm(interface)

    if tool == "4":
        clear()
        beacon_thief()

    if tool == "5":
        clear()
        my_hash = input("hash\n")
        brute_force_hash(my_hash)

    if tool == "6":
        clear()
        my_file = input("file\n")
        my_hash = input("hash\n")
        dictionary_hash(my_file, my_hash, mask=True)

    if tool == "7":
        clear()
        file = input("file\n")
        hex_viewer(file)

    if tool == "8":
        clear()
        username = input("username\n")
        accounts = osint(username)
        for account in accounts:
            print(CYAN + account)

    if tool == "9":
        clear()
        packet_sniffer(data=True, hex_dump=True)

    if tool == "10":
        clear()
        device = input("file, folder, or device\n")
        secure_overwrite(device)

    if tool == "11":
        clear()
        file = input("file\n")
        source_code_viewer(file)

    if tool == "12":
        clear()
        host = input("host\n")
        print(web_scanner(host))

main()
