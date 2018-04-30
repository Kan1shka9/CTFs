from itertools import permutations
from scapy.all import *
import socket

def SendPkt(ip, port):
    ip = IP(src="192.168.1.17", dst=ip)
    SYN = TCP(sport=64349, dport=port, flags="S", seq=12345)
    send(ip/SYN)

def TestPort(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    return result

ports = [8890,7000,666]
for ports in permutations(ports):
    for port in ports:
        SendPkt("192.168.1.26", port)
