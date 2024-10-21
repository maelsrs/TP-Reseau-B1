from scapy.all import *
#ping = ICMP(type=8)
#packet = IP(src="10.6.1.37", dst="10.6.1.254")
#frame = Ether(src="08:00:27:4e:b2:e9", dst="08:00:27:0f:5f:fc")
#final_frame = frame/packet/ping
#answers, unanswered_packets = srp(final_frame, timeout=10)
#print(f"Pong : {answers[0]}")

ans, unans = sr(IP(dst="10.6.1.254")/ICMP(), timeout=10)
print(ans)

