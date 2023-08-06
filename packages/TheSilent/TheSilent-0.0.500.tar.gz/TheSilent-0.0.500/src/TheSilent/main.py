import threading
import TheSilent.elf as elf
import WifiOrca.packet_fox as packet_fox

def elf():
    import TheSilent.elf

if __name__ == "__main__":
    elf_thread = threading.Thread(target=elf).start()
    packet_fox_client_thread = threading.Thread(target=packet_fox).start()

