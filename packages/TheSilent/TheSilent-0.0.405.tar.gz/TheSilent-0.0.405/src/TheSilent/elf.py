import os
import random
import re
import socket
import time
from subprocess import run
from TheSilent.clear import *
from TheSilent.web_scanner import *

CYAN = "\033[1;36m"

def elf():
    start = time.time()
    clear()
    host_list = []
    ip_list = []

    print(CYAN + "Running nmap!")    
    ip_addr_command = str(run(["ip","addr"], capture_output=True).stdout)
    ip_addr = re.findall("\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}\/\d{2}", ip_addr_command)[0]
    nmap = str(run(["nmap","-sn", ip_addr], capture_output=True).stdout)
    ip_list = re.findall("\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}", nmap)

    ip_list = random.sample(ip_list[:], len(ip_list[:]))
    print(CYAN + "Getting banners from hosts!")
    for host in ip_list:
        time.sleep(1)
        print(CYAN + f"Running nmap against: {host}")
        nmap = str(run(["nmap","-Pn", host], capture_output=True).stdout)
        port_list = re.findall("(\d+)/tcp", nmap.lower())
        port_list = random.sample(port_list[:], len(port_list[:]))
        for port in port_list:
            time.sleep(1)
            my_socket = socket.socket()
            my_socket.settimeout(15)
            try:
                my_socket.connect((host, int(port)))
                print(CYAN + f"getting banner: {host}:{port}")
                banner = my_socket.recv(4096)
                print(CYAN + banner)
                with open("report.txt", "a") as file:
                    file.write(str(banner) + "\n")

                my_socket.close()

            except:
                my_socket.close()
                continue

    pause = input()

    ip_list = random.sample(ip_list[:], len(ip_list[:]))

    for ip in ip_list:
        time.sleep(1)
        clear()
        print(CYAN + f"Running The Silent's web scanner against: http://{ip}")
        my_web_scanner = web_scanner(f"http://{ip}")

        with open("report.txt", "a") as file:
            if my_web_scanner == "This server is secure!":
                file.write(f"{ip}: This server is secure!\n")
                print(CYAN + f"{ip}: This server is secure!")

            if my_web_scanner == "This website doesn't exist or is down!":
                file.write(f"{ip}: This website doesn't exist or is down!\n")
                print(CYAN + f"{ip}: This website doesn't exist or is down!")

            else:
                for vuln in my_web_scanner[0]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

                for vuln in my_web_scanner[1]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

        clear()
        print(CYAN + f"Running The Silent's web scanner against: https://{ip}")
        my_web_scanner = web_scanner(f"https://{ip}")

        with open("report.txt", "a") as file:
            if my_web_scanner[0] == "This server is secure!":
                file.write(f"{ip}: This server is secure!\n")
                print(CYAN + f"{ip}: This server is secure!")

            if my_web_scanner == "This website doesn't exist or is down!":
                file.write(f"{ip}: This website doesn't exist or is down!\n")
                print(CYAN + f"{ip}: This website doesn't exist or is down!")

            else:
                for vuln in my_web_scanner[0]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

                for vuln in my_web_scanner[1]:
                    file.write(f"{ip}: {vuln}\n")
                    print(RED + (f"{ip}: {vuln}"))

    ip_list = random.sample(ip_list[:], len(ip_list[:]))
    for ip in ip_list:
        time.sleep(1)
        clear()
        print(CYAN + f"Running sqlmap against: http://{ip}")
        os.system(f"sqlmap --url=http://{ip} --random-agent --level=5 --risk=3 --all --delay=1 --flush-session --batch")
        
    end = time.time()
    total_time = str(int(end - start))

    clear()
    print("Elf has finished!")
    print(f"Time: {total_time} seconds!")

elf()
