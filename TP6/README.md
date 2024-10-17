# TP6 : Des bo services dans des bo LANs

## Sommaire

- [TP6 : Des bo services dans des bo LANs](#tp6--des-bo-services-dans-des-bo-lans)
  - [Sommaire](#sommaire)
- [I. Le setup](#i-le-setup)
  - [1. Tableau d'adressage](#1-tableau-dadressage)
  - [2. Marche à suivre](#2-marche-à-suivre)
- [II. LAN clients](#ii-lan-clients)
  - [2. Client](#2-client)
- [III. LAN serveurzzzz](#iii-lan-serveurzzzz)
  - [1. Serveur Web](#1-serveur-web)
  - [2. Serveur DNS](#2-serveur-dns)
  - [3. Serveur DHCP](#3-serveur-dhcp)

# I. Le setup

## 1. Tableau d'adressage

## 2. Marche à suivre

**☀️ Prouvez que...**

- une machine du LAN1 peut joindre internet (ping un nom de domaine)
```powershell
[mael@dhcp ~]$ ping ynov.com
PING ynov.com (104.26.11.233) 56(84) bytes of data.
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=1 ttl=53 time=18.1 ms
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=2 ttl=53 time=18.3 ms
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=3 ttl=53 time=17.7 ms
```
- une machine du LAN2 peut joindre internet (ping nom de domaine)
```powershell
[mael@web ~]$ ping ynov.com
PING ynov.com (104.26.11.233) 56(84) bytes of data.
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=1 ttl=53 time=20.2 ms
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=2 ttl=53 time=17.9 ms
64 bytes from 104.26.11.233 (104.26.11.233): icmp_seq=3 ttl=53 time=33.6 ms
```
- une machine du LAN1 peut joindre une machine du LAN2 (ping une adresse IP)
```powershell
[mael@dhcp ~]$ ping 10.6.2.12
PING 10.6.2.12 (10.6.2.12) 56(84) bytes of data.
64 bytes from 10.6.2.12: icmp_seq=1 ttl=63 time=1.57 ms
64 bytes from 10.6.2.12: icmp_seq=2 ttl=63 time=1.62 ms
64 bytes from 10.6.2.12: icmp_seq=3 ttl=63 time=3.54 ms
```

# II. LAN clients

## 2. Client

**☀️ Prouvez que...**

- le client a bien récupéré une adresse IP en DHCP

```powershell
mael@client1:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:fd:d1:20 brd ff:ff:ff:ff:ff:ff
    inet 10.6.1.37/24 brd 10.6.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 43043sec preferred_lft 43043sec
    inet6 fe80::150b:49ef:fec2:5648/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```
- vous avez bien 1.1.1.1 en DNS

```powershell
mael@client1:~$ resolvectl
Global
         Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
  resolv.conf mode: stub

Link 2 (enp0s8)
    Current Scopes: DNS
         Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 1.1.1.1
       DNS Servers: 1.1.1.1
```
- vous avez bien la bonne passerelle indiquée
```powershell
mael@client1:~$ ip r s
default via 10.6.1.254 dev enp0s8 proto dhcp src 10.6.1.38 metric 100
```
- que ça ping un nom de domaine public sans problème magueule
```powershell
mael@client1:~$ ping ynov.com
PING ynov.com (104.26.10.233) 56(84) bytes of data.
64 bytes from 104.26.10.233: icmp_seq=1 ttl=53 time=17.2 ms
64 bytes from 104.26.10.233: icmp_seq=2 ttl=53 time=18.9 ms
64 bytes from 104.26.10.233: icmp_seq=3 ttl=53 time=19.1 ms
```



# III. LAN serveurzzzz

## 1. Serveur Web

**☀️ Déterminer sur quel port écoute le serveur NGINX**

```powershell
[mael@web ~]$ sudo ss -lnpt | grep 80
LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=1503,fd=6),("nginx",pid=1502,fd=6))
LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=1503,fd=7),("nginx",pid=1502,fd=7))
```

**☀️ Ouvrir ce port dans le firewall**

```powershell
[mael@web ~]$ sudo firewall-cmd --permanent --add-port=80/tcp
success
[mael@web ~]$ sudo firewall-cmd --reload
success
```

**☀️ Visitez le site web !**

```powershell
mael@client1:~$ curl 10.6.2.11:80
<!doctype html>
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>HTTP Server Test Page powered by: Rocky Linux</title>
    <style type="text/css">
    [...]
  </style>
  </head>
  <body>
    <h1>HTTP Server <strong>Test Page</strong></h1>
    [...]
  </body>
</html>
```
## 2. Serveur DNS

**☀️ Déterminer sur quel(s) port(s) écoute le service BIND9**
```powershell
[root@dns mael]# sudo ss -lnpt | grep 53
LISTEN 0      10         127.0.0.1:53        0.0.0.0:*    users:(("named",pid=1951,fd=22))
LISTEN 0      10         10.6.2.12:53        0.0.0.0:*    users:(("named",pid=1951,fd=25))
LISTEN 0      4096       127.0.0.1:953       0.0.0.0:*    users:(("named",pid=1951,fd=28))
LISTEN 0      4096           [::1]:953          [::]:*    users:(("named",pid=1951,fd=29))
LISTEN 0      10             [::1]:53           [::]:*    users:(("named",pid=1951,fd=27))
[root@dns mael]# sudo ss -lnpu | grep 53
UNCONN 0      0          10.6.2.12:53        0.0.0.0:*    users:(("named",pid=1951,fd=24))
UNCONN 0      0          127.0.0.1:53        0.0.0.0:*    users:(("named",pid=1951,fd=21))
UNCONN 0      0              [::1]:53           [::]:*    users:(("named",pid=1951,fd=26))
```

**☀️ Ouvrir ce(s) port(s) dans le firewall**

```powershell
[root@dns etc]# sudo firewall-cmd --permanent --add-port=53/tcp
success
[root@dns etc]# sudo firewall-cmd --permanent --add-port=53/udp
success
[root@dns etc]# sudo firewall-cmd --reload
success
```

**☀️ Effectuez des requêtes DNS manuellement depuis le serveur DNS lui-même dans un premier temps**

```powershell
[root@dns mael]# dig web.tp6.b1 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> web.tp6.b1 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5604
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: a51f5f49b4ca8d7301000000670f9616ee602906f3efb12b (good)
;; QUESTION SECTION:
;web.tp6.b1.                    IN      A

;; ANSWER SECTION:
web.tp6.b1.             86400   IN      A       10.6.2.11

;; Query time: 0 msec
;; SERVER: 10.6.2.12#53(10.6.2.12)
;; WHEN: Wed Oct 16 12:31:50 CEST 2024
;; MSG SIZE  rcvd: 83

[root@dns mael]# dig dns.tp6.b1 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> dns.tp6.b1 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41368
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: a30179ce44d9139d01000000670f96639d05adcd616fbb52 (good)
;; QUESTION SECTION:
;dns.tp6.b1.                    IN      A

;; ANSWER SECTION:
dns.tp6.b1.             86400   IN      A       10.6.2.12

;; Query time: 0 msec
;; SERVER: 10.6.2.12#53(10.6.2.12)
;; WHEN: Wed Oct 16 12:33:07 CEST 2024
;; MSG SIZE  rcvd: 83

[root@dns mael]# dig ynov.com @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> ynov.com @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 38441
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: e2698bd07a6c726a01000000670f967d47bbe6e6555cb1d9 (good)
;; QUESTION SECTION:
;ynov.com.                      IN      A

;; ANSWER SECTION:
ynov.com.               300     IN      A       172.67.74.226
ynov.com.               300     IN      A       104.26.10.233
ynov.com.               300     IN      A       104.26.11.233

;; Query time: 266 msec
;; SERVER: 10.6.2.12#53(10.6.2.12)
;; WHEN: Wed Oct 16 12:33:33 CEST 2024
;; MSG SIZE  rcvd: 113

[root@dns mael]# dig -x 10.6.2.11 @10.6.2.12

; <<>> DiG 9.16.23-RH <<>> -x 10.6.2.11 @10.6.2.12
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 34490
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 384498434d177b76010000006710df49656e45eb5c247e72 (good)
;; QUESTION SECTION:
;11.2.6.10.in-addr.arpa.                IN      PTR

;; ANSWER SECTION:
11.2.6.10.in-addr.arpa. 86400   IN      PTR     web.tp6.b1.

;; Query time: 0 msec
;; SERVER: 10.6.2.12#53(10.6.2.12)
;; WHEN: Thu Oct 17 11:56:25 CEST 2024
;; MSG SIZE  rcvd: 103
```

**☀️ Effectuez une requête DNS manuellement depuis client1.tp6.b1**

```powershell
mael@client1:~$ drill ynov.com @10.6.2.12
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 57014
;; flags: qr rd ra ; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 0
;; QUESTION SECTION:
;; ynov.com.    IN      A

;; ANSWER SECTION:
ynov.com.       300     IN      A       104.26.10.233
ynov.com.       300     IN      A       104.26.11.233
ynov.com.       300     IN      A       172.67.74.226

;; AUTHORITY SECTION:

;; ADDITIONAL SECTION:

;; Query time: 24 msec
;; SERVER: 10.6.2.12
;; WHEN: Wed Oct 16 12:50:35 2024
;; MSG SIZE  rcvd: 74
mael@client1:~$ drill web.tp6.b1 @10.6.2.12
;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 53764
;; flags: qr aa rd ra ; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
;; QUESTION SECTION:
;; web.tp6.b1.  IN      A

;; ANSWER SECTION:
web.tp6.b1.     86400   IN      A       10.6.2.11

;; AUTHORITY SECTION:

;; ADDITIONAL SECTION:

;; Query time: 2 msec
;; SERVER: 10.6.2.12
;; WHEN: Wed Oct 16 12:51:30 2024
;; MSG SIZE  rcvd: 44
```
**☀️ Capturez une requête DNS et la réponse de votre serveur**

[Fichier dns.pcap](dns.pcap)

## 3. Serveur DHCP

**☀️ Créez un nouveau client client2.tp6.b1 vitefé**

- récupérez une IP en DHCP sur ce nouveau client2.tp6.b1

- vérifiez que vous avez bien 10.6.2.12 comme serveur DNS à contacter

- Vous devriez pouvoir visiter http://web.tp6.b1 avec le navigateur, ça devrait fonctionner sans aucune autre action.