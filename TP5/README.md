# TP5 : Un ptit LAN à nous

## Sommaire

- [TP5 : Un ptit LAN à nous](#tp5--un-ptit-lan-à-nous)
  - [Sommaire](#sommaire)
- [I. Setup](#i-setup)
- [II. Accès internet pour tous](#ii-accès-internet-pour-tous)
  - [1. Accès internet routeur](#1-accès-internet-routeur)
  - [2. Accès internet clients](#2-accès-internet-clients)
- [III. Serveur SSH](#iii-serveur-ssh)
- [IV. Serveur DHCP](#iv-serveur-dhcp)
  - [3. Rendu attendu](#3-rendu-attendu)
    - [A. Installation et configuration du serveur DHCP](#a-installation-et-configuration-du-serveur-dhcp)
    - [B. Test avec un nouveau client](#b-test-avec-un-nouveau-client)
    - [C. Consulter le bail DHCP](#c-consulter-le-bail-dhcp)

# I. Setup

**☀️ Uniquement avec des commandes, prouvez-que :**

- vous avez bien configuré les adresses IP demandées (un `ip a` suffit hein)
 ```powershell
 [root@routeur mael]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:66:52:66 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.254/24 brd 10.5.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe66:5266/64 scope link
       valid_lft forever preferred_lft forever
```
```powershell
mael@client1~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:0a:5a:44 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.11/24 brd 10.5.1.255 scope global enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe0a:5a44/64 scope link
       valid_lft forever preferred_lft forever
```
```powershell
mael@client2:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:05:e4:09 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.12/24 brd 10.5.1.255 scope global enp0s8
       valid_lft forever preferred_lft forever
```

***Les hostnames sont configurés (visibles au dessus)***
- tout le monde peut se ping au sein du réseau `10.5.1.0/24`

```powershell
[root@routeur mael]# ping 10.5.1.11
PING 10.5.1.11 (10.5.1.11) 56(84) bytes of data.
64 bytes from 10.5.1.11: icmp_seq=1 ttl=64 time=0.622 ms

[root@routeur mael]# ping 10.5.1.12
PING 10.5.1.12 (10.5.1.12) 56(84) bytes of data.
64 bytes from 10.5.1.12: icmp_seq=1 ttl=64 time=0.646 ms

mael@client1:~$ ping 10.5.1.254
PING 10.5.1.254 (10.5.1.254) 56(84) bytes of data.
64 bytes from 10.5.1.254: icmp_seq=1 ttl=64 time=1.94 ms

mael@client1:~$ ping 10.5.1.12
PING 10.5.1.12 (10.5.1.12) 56(84) bytes of data.
64 bytes from 10.5.1.12: icmp_seq=1 ttl=64 time=0.467 ms

mael@client2:~$ ping 10.5.1.254
PING 10.5.1.254 (10.5.1.254) 56(84) bytes of data.
64 bytes from 10.5.1.254: icmp_seq=1 ttl=64 time=1.46 ms

mael@client2:~$ ping 10.5.1.11
PING 10.5.1.11 (10.5.1.11) 56(84) bytes of data.
64 bytes from 10.5.1.11: icmp_seq=1 ttl=64 time=1.33 ms
```

# II. Accès internet pour tous

## 1. Accès internet routeur

☀️ **Déjà, prouvez que le routeur a un accès internet**

```powershell
[root@routeur mael]# ping ynov.com
PING ynov.com (172.67.74.226) 56(84) bytes of data.
64 bytes from 172.67.74.226 (172.67.74.226): icmp_seq=1 ttl=54 time=21.5 ms
```

**☀️ Activez le routage**

```powershell
[root@routeur mael]# sudo firewall-cmd --add-masquerade --permanent
success
[root@routeur mael]# sudo firewall-cmd --reload
success
```
## 2. Accès internet clients

☀️ **Prouvez que les clients ont un accès internet**

 ```powershell
root@client1:/home/mael# ping 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=50 time=183 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=50 time=49.8 ms
64 bytes from 1.1.1.1: icmp_seq=3 ttl=50 time=337 ms
```

```powershell
root@client2:/home/mael# ping ynov.com
PING ynov.com (104.26.10.233) 56(84) bytes of data.
64 bytes from 104.26.10.233: icmp_seq=1 ttl=50 time=116 ms
```

☀️ **Montrez-moi le contenu final du fichier de configuration de l'interface réseau**

```yaml
mael@client2:~$ cat /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: no
      addresses: [10.5.1.12/24]
      gateway4: 10.5.1.254
      nameservers:
        addresses: [1.1.1.1,1.0.0.1]
```
# III. Serveur SSH

☀️ **Sur `routeur.tp5.b1`, déterminer sur quel port écoute le serveur SSH**

```powershell
[root@routeur mael]# sudo ss -lnpt | grep 22
LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=660,fd=3))
LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=660,fd=4))
```

☀️ **Sur `routeur.tp5.b1`, vérifier que ce port est bien ouvert**

*verifier que le port est ouvert, en étant actuellement connecté en ssh, c'est drôle*

firewalld autorise les connexions au service ssh, et iptables ne bloque rien, alors le port ssh est ouvert.
```powershell
[root@routeur mael]# sudo firewall-cmd --list-all
public (active)
[...]
  interfaces: enp0s3 enp0s8
  services: dhcp dhcpv6-client ssh
  forward: yes
  masquerade: yes
[...]
```

# IV. Serveur DHCP

## 3. Rendu attendu

### A. Installation et configuration du serveur DHCP

☀️ **Installez et configurez un serveur DHCP sur la machine `routeur.tp5.b1`**

```powershell
[root@routeur mael]# dnf install -y dhcp-server
[...]
Complete!
```

```powershell
[root@routeur mael]# cat /etc/dhcp/dhcpd.conf
authoritative;
subnet 10.5.1.0 netmask 255.255.255.0 {
    range 10.5.1.137 10.5.1.237;
    option broadcast-address 10.5.1.255;
    option routers 10.5.1.254;
    option domain-name-servers 1.1.1.1;
}
```

```powershell
[root@routeur mael]# cat /etc/sysconfig/network-scripts/ifcfg-enp0s8
DEVICE=enp0s8
NAME=len

ONBOOT=yes
BOOTPROTO=static

IPADDR=10.5.1.254
NETMASK=255.255.255.0
GATEWAY=10.5.1.254
DNS1=1.1.1.1
```

### B. Test avec un nouveau client

### C. Consulter le bail DHCP

☀️ **Consultez le *bail DHCP* qui a été créé pour notre client**

```powershell
[root@routeur mael]# cat /var/lib/dhcpd/dhcpd.leases
lease 10.5.1.139 {
  starts 2 2024/10/15 11:15:26;
  ends 2 2024/10/15 23:15:26;
  cltt 2 2024/10/15 11:15:26;
  binding state active;
  next binding state free;
  rewind binding state free;
  hardware ethernet 08:00:27:85:ab:d4;
  uid "\377\257\201\217}\000\002\000\000\253\021\203\264\337g\347\206\211;";
  client-hostname "client3.tp5.b1";
}
```

☀️ **Confirmez qu'il s'agit bien de la bonne adresse MAC**

```powershell
mael@client3:~$ ip a
[...]
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:85:ab:d4 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.139/24 metric 100 brd 10.5.1.255 scope global dynamic enp0s8
       valid_lft 42352sec preferred_lft 42352sec
    inet6 fe80::a00:27ff:fe85:abd4/64 scope link
       valid_lft forever preferred_lft forever
```

# Bonus

ça arrive 🌏...