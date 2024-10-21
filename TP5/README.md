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

**☀️ Créez une nouvelle machine client client3.tp5.b1**

- définissez son hostname

```powershell
mael@mael-vb:~$ sudo hostnamectl set-hostname client3.tp5.b1
[sudo] password for mael:
mael@mael-vb:~$
```

- définissez une IP en DHCP

```powershell
mael@client3:~$ cat /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      dhcp4: yes

mael@client3:~$ sudo netplan apply
[sudo] password for mael:

** (generate:5104): WARNING **: 16:21:48.702: Permissions for /etc/netplan/01-netcfg.yaml are too open. Netplan configuration should NOT be accessible by others.

** (process:5103): WARNING **: 16:21:48.996: Permissions for /etc/netplan/01-netcfg.yaml are too open. Netplan configuration should NOT be accessible by others.

** (process:5103): WARNING **: 16:21:49.079: Permissions for /etc/netplan/01-netcfg.yaml are too open. Netplan configuration should NOT be accessible by others.
mael@client3:~$
```

- vérifiez que c'est bien une adresse IP entre .137 et .237
```powershell
mael@client3:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:85:ab:d4 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.139/24 metric 100 brd 10.5.1.255 scope global dynamic enp0s8
       valid_lft 43154sec preferred_lft 43154sec
    inet6 fe80::a00:27ff:fe85:abd4/64 scope link
       valid_lft forever preferred_lft forever

```
- prouvez qu'il a immédiatement un accès internet
```powershell
mael@client3:~$ ping ynov.com
PING ynov.com (104.26.11.233) 56(84) bytes of data.
64 bytes from 104.26.11.233: icmp_seq=1 ttl=54 time=14.3 ms
64 bytes from 104.26.11.233: icmp_seq=2 ttl=54 time=13.6 ms
64 bytes from 104.26.11.233: icmp_seq=3 ttl=54 time=17.8 ms
```
### C. Consulter le bail DHCP

☀️ **Consultez le *bail DHCP* qui a été créé pour notre client**

```powershell
[root@routeur mael]# cat /var/lib/dhcpd/dhcpd.leases
[...]
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

## DHCP spoofing

**☀️ Installer et configurer un serveur DHCP sur la machine attaquante**

```powershell
mael@client2:~/dhcp-spoof$ sudo cat /etc/dnsmasq.conf
dhcp-authoritative
dhcp-leasefile=/tmp/dhcp.leases

# use /etc/ethers for static hosts; same format as --dhcp-host
read-ethers

# Plage DHCP
dhcp-range=10.5.1.240,10.5.1.250,12h
# Netmask
dhcp-option=1,255.255.255.0
# Route
dhcp-option=3,10.5.1.1
```

**☀️ Depuis un autre client, demander un adresse IP en DHCP**

- déterminer si vous avez une adresse IP proposée par le vrai serveur DHCP ou la machine de l'attaquant

Le vrai serveur DHCP est arrivé plus vite et on a donc reçu les réponses par lui

[Fichier dhcp_spoof.pcap](dhcp_spoof.pcap)

**☀️ Pour que ça marche mieux, il faut flood le serveur DHCP réel**

Avec le script de flood du deuxième bonus et avec un certain nombre d'essais, l'attaquant a envoyé ses requêtes avant, et donc le DHCP Spoofing est réussi.

```powershell
mael@client3:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:85:ab:d4 brd ff:ff:ff:ff:ff:ff
    inet 10.5.1.249/24 brd 10.5.1.255 scope global dynamic enp0s8
       valid_lft 43011sec preferred_lft 43011sec
    inet6 fe80::a00:27ff:fe85:abd4/64 scope link
       valid_lft forever preferred_lft forever
```

## Flood protection

☀️ Lancer mon super script qui super flood

```powershell
mael@client2:~$ wget https://gitlab.com/it4lik/b1-network-2024/-/raw/main/tp/5/flood.sh
--2024-10-21 11:27:52--  https://gitlab.com/it4lik/b1-network-2024/-/raw/main/tp/5/flood.sh
Resolving gitlab.com (gitlab.com)... 172.65.251.78, 2606:4700:90:0:f22e:fbec:5bed:a9b9
Connecting to gitlab.com (gitlab.com)|172.65.251.78|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 562 [text/plain]
Saving to: ‘flood.sh’

flood.sh                      100%[=================================================>]     562  --.-KB/s    in 0s

2024-10-21 11:27:52 (148 MB/s) - ‘flood.sh’ saved [562/562]


mael@client2:~$ chmod +x flood.sh
mael@client2:~$ bash flood.sh
Let's flood 10.5.1.254:22
```

**☀️ Lister les connexions TCP actives**

```
[mael@routeur ~]$ ss -atn
State            Recv-Q       Send-Q             Local Address:Port              Peer Address:Port        Process
LISTEN           0            128                      0.0.0.0:22                     0.0.0.0:*
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:34448
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:34592
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:34522
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:41538
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:41564
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:41598
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:41562
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:34438
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:41500
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:41646
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:34558
FIN-WAIT-2       0            0                     10.5.1.254:22                   10.5.1.12:34498
ESTAB            0            0                     10.5.1.254:22                   10.5.1.12:34474
[...]
```

**☀️ Trouver le fichier de logs du service SSH**

```powershell
[root@routeur log]# cat /var/log/secure | grep 10.5.1.12
[...]
Oct 21 11:50:22 routeur sshd[2207]: Connection reset by 10.5.1.12 port 43038
Oct 21 11:50:23 routeur sshd[2209]: Connection reset by 10.5.1.12 port 43984
Oct 21 11:50:23 routeur sshd[2210]: Connection reset by 10.5.1.12 port 43988
Oct 21 11:50:23 routeur sshd[2208]: Connection reset by 10.5.1.12 port 43966
Oct 21 11:50:23 routeur sshd[2211]: Connection reset by 10.5.1.12 port 44004
Oct 21 11:50:24 routeur sshd[2212]: Connection reset by 10.5.1.12 port 44006
Oct 21 11:50:24 routeur sshd[2213]: Connection reset by 10.5.1.12 port 44022
Oct 21 11:50:24 routeur sshd[2214]: Connection reset by 10.5.1.12 port 44028
Oct 21 11:50:25 routeur sshd[2215]: Connection reset by 10.5.1.12 port 44054
Oct 21 11:50:25 routeur sshd[2218]: Connection reset by 10.5.1.12 port 44088
Oct 21 11:50:25 routeur sshd[2216]: Connection reset by 10.5.1.12 port 44060
Oct 21 11:50:25 routeur sshd[2217]: Connection reset by 10.5.1.12 port 44068
Oct 21 11:50:26 routeur sshd[2219]: Connection reset by 10.5.1.12 port 44118
Oct 21 11:50:27 routeur sshd[2220]: Connection reset by 10.5.1.12 port 44176
Oct 21 11:50:27 routeur sshd[2221]: Connection reset by 10.5.1.12 port 44190
[...]
```

**☀️ Repérer et ban la source du flood**

- utiliser une commande firewall-cmd pour ban l'adresse IP de la source

```powershell
[root@routeur log]# sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.5.1.12" reject'
success
[root@routeur log]# sudo firewall-cmd --reload
success
```

Sur le client, on ne peut plus envoyer de requêtes:

```powershell
flood.sh: line 18: /dev/tcp/10.5.1.254/22: Connection refused
flood.sh: connect: Connection refused
```

**☀️ Installer fail2ban sur routeur.tp5.b1**

```powershell
[root@routeur log]# sudo dnf install epel-release -y
[...]
Installed:
  epel-release-9-7.el9.noarch

Complete!

[root@routeur log]# sudo dnf install fail2ban -y
[...]

Installed:
  checkpolicy-3.6-1.el9.x86_64                          esmtp-1.2-19.el9.x86_64
  fail2ban-1.0.2-12.el9.noarch                          fail2ban-firewalld-1.0.2-12.el9.noarch
  fail2ban-selinux-1.0.2-12.el9.noarch                  fail2ban-sendmail-1.0.2-12.el9.noarch
  fail2ban-server-1.0.2-12.el9.noarch                   libesmtp-1.0.6-24.el9.x86_64
  liblockfile-1.14-10.el9.0.1.x86_64                    policycoreutils-python-utils-3.6-2.1.el9.noarch
  python3-audit-3.1.2-2.el9.x86_64                      python3-distro-1.5.0-7.el9.noarch
  python3-libsemanage-3.6-1.el9.x86_64                  python3-policycoreutils-3.6-2.1.el9.noarch
  python3-setools-4.4.4-1.el9.x86_64                    python3-setuptools-53.0.0-12.el9_4.1.noarch

Complete!
```

```powershell
[root@routeur log]# cat /etc/fail2ban/jail.d/ssh.conf
[DEFAULT]
bantime = 1h

[sshd]
enabled = true
```

```powershell
[root@routeur log]# sudo fail2ban-client status sshd
Status for the jail: sshd
|- Filter
|  |- Currently failed: 0
|  |- Total failed:     0
|  `- Journal matches:  _SYSTEMD_UNIT=sshd.service + _COMM=sshd
`- Actions
   |- Currently banned: 0
   |- Total banned:     0
   `- Banned IP list:
```