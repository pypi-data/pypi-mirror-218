import socket

def packet_fox_server():
    my_socket = socket.socket()
    my_socket.bind(("",80))
    my_socket.listen(5)
    print("listening")
    while True:
        conn, addr = my_socket.accept()
        data = conn.recv(65536).decode()
        with open("hex_dump.txt", "a") as file:
            file.write(data + "\n")

packet_fox_server()
