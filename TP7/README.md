# TP7 : On dit chiffrer pas crypter


## Sommaire

- [TP7 : On dit chiffrer pas crypter](#tp7--on-dit-chiffrer-pas-crypter)
  - [Sommaire](#sommaire)
- [II. Serveur Web](#ii-serveur-web)
  - [1. HTTP](#1-http)
    - [B. Configuration](#b-configuration)
    - [C. Tests client](#c-tests-client)
    - [D. Analyze](#d-analyze)
  - [2. On rajoute un S](#2-on-rajoute-un-s)
    - [A. Config](#a-config)
    - [B. Test test test analyyyze](#b-test-test-test-analyyyze)

- [III. Serveur VPN](#iii-serveur-vpn)

  - [1. Install et conf Wireguard](#1-install-et-conf-wireguard)
  - [3. Proofs](#3-proofs)
  - [4. Private service](#4-private-service)

# II. Serveur Web
## 1. HTTP

### B. Configuration
🌞 **Lister les ports en écoute sur la machine**

```powershell
[root@web mael]# sudo ss -lnpt | grep "80"
LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=1629,fd=6),("nginx",pid=1628,fd=6))
LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=1629,fd=7),("nginx",pid=1628,fd=7))
```

🌞 **Ouvrir le port dans le firewall de la machine**

```powershell
[root@web mael]# sudo firewall-cmd --permanent --add-port=80/tcp
success
[root@web mael]# sudo firewall-cmd --reload
success
```

### C. Tests client
🌞 **Vérifier que ça a pris effet**
- faites un ping vers sitedefou.tp7.b1
```powershell
root@client1:/home/mael# ping sitedefou.tp7.b1
PING sitedefou.tp7.b1 (10.7.1.11) 56(84) bytes of data.
64 bytes from sitedefou.tp7.b1 (10.7.1.11): icmp_seq=1 ttl=64 time=0.777 ms
64 bytes from sitedefou.tp7.b1 (10.7.1.11): icmp_seq=2 ttl=64 time=0.972 ms
64 bytes from sitedefou.tp7.b1 (10.7.1.11): icmp_seq=3 ttl=64 time=0.581 ms
64 bytes from sitedefou.tp7.b1 (10.7.1.11): icmp_seq=4 ttl=64 time=0.954 ms
```
- visitez http://sitedefou.tp7.b1 
```powershell
root@client1:/home/mael# curl http://sitedefou.tp7.b1
meow !
```


### D. Analyze
🌞 **Capture `tcp_http.pcap`**

[Fichier tcp_http.pcap](tcp_http.pcap)

🌞 **Voir la connexion établie**

```powershell
mael@client1:~$ ss -atn | grep "80"
TIME-WAIT 0      0               10.7.1.101:39012         10.7.1.11:80
LISTEN    0      511                      *:8080                  *:*
```

## 2. On rajoute un S

### A. Config

🌞 **Lister les ports en écoute sur la machine**

```powershell
[root@web mael]# sudo ss -lnpt | grep "443"
LISTEN 0      511        10.7.1.11:443       0.0.0.0:*    users:(("nginx",pid=1708,fd=6),("nginx",pid=1707,fd=6))
```
🌞 **Gérer le firewall**

```powershell
[root@web mael]# sudo firewall-cmd --permanent --add-port=443/tcp
success
[root@web mael]# sudo firewall-cmd --reload
success
```
### B. Test test test analyyyze
🌞 **Capture `tcp_https.pcap`**

[Fichier tcp_https.pcap](tcp_https.pcap)

# III. Serveur VPN
## 1. Install et conf Wireguard

🌞 **Prouvez que vous avez bien une nouvelle carte réseau `wg0`**

```powershell
[root@vpn mael]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:4f:18:4e brd ff:ff:ff:ff:ff:ff
    inet 10.7.1.111/8 brd 10.255.255.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe4f:184e/64 scope link
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a4:60:9f brd ff:ff:ff:ff:ff:ff
    inet 10.7.2.111/8 brd 10.255.255.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fea4:609f/64 scope link
       valid_lft forever preferred_lft forever
4: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 10.7.200.1/24 scope global wg0
       valid_lft forever preferred_lft forever
```

🌞 **Déterminer sur quel port écoute Wireguard**

```powershell
[root@vpn mael]# sudo ss -lupn | grep 51820
UNCONN 0      0            0.0.0.0:51820      0.0.0.0:*
UNCONN 0      0               [::]:51820         [::]:*
```

🌞 **Ouvrez ce port dans le firewall**

```powershell
[root@web mael]# sudo firewall-cmd --permanent --add-port=51820/udp
success
[root@web mael]# sudo firewall-cmd --reload
success
```

## 3. Proofs
🌞 **Ping ping ping !**

```powershell
root@client1:/home/mael# ping 10.7.200.1
PING 10.7.200.1 (10.7.200.1) 56(84) bytes of data.
64 bytes from 10.7.200.1: icmp_seq=1 ttl=64 time=1.67 ms
64 bytes from 10.7.200.1: icmp_seq=2 ttl=64 time=1.12 ms
64 bytes from 10.7.200.1: icmp_seq=3 ttl=64 time=1.66 ms
64 bytes from 10.7.200.1: icmp_seq=4 ttl=64 time=1.95 ms
```

🌞 **Capture `ping1_vpn.pcap`**

[Fichier ping1_vpn.pcap](ping1_vpn.pcap)

🌞 **Prouvez que vous avez toujours un accès internet**

```powershell
mael@client1:~$ traceroute 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 30 hops max, 60 byte packets
 1  _gateway (10.7.200.1)  3.232 ms  3.253 ms  3.757 ms
 2  10.7.1.254 (10.7.1.254)  3.737 ms  5.388 ms  5.412 ms
 3  10.0.2.2 (10.0.2.2)  6.197 ms  6.113 ms  5.881 ms
 4  * * *
 5  * * *
 6  * * *
 7  * * *
 8  * * *
 9  * * *
10  * * *
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  * * *
21  * * *
22  * * *
23  * * *
24  * * *
25  * * *
26  * * *
27  * * *
28  * * *
29  * * *
30  * * *
```
## 4. Private service

🌞 **Visitez le service Web à travers le VPN**

