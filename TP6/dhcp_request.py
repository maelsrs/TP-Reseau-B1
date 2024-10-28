import random
from scapy.all import *

def mac_to_bytes(mac_addr: str) -> bytes:
    return int(mac_addr.replace(":", ""), 16).to_bytes(6, "big")

client_mac = "08:00:27:4e:b2:e9"
targetIp = "10.6.1.102"
interface = "enp0s8"

packet = (
    Ether(dst="ff:ff:ff:ff:ff:ff") /
    IP(src="0.0.0.0", dst="255.255.255.255") /
    UDP(sport=68, dport=67) /
    BOOTP(
        chaddr=mac_to_bytes(client_mac),
        xid=random.randint(1, 2**32-1),
    ) /
    DHCP(options=[("message-type", "discover"),("requested_addr", targetIp), "end"])
)
sendp(packet, iface=interface, verbose=False)

def filter_ack(pkt):
    return (
        pkt.haslayer(DHCP)
        and pkt[DHCP].options[0][1] == 5
        and pkt[BOOTP].xid == transaction_id
    )

ack = sniff(filter="udp and port 67", iface=interface, timeout=10, count=1, lfilter=filter_ack)
if ack:
    print("ACK reçu")