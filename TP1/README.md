# TP1 : Les premiers pas de bébé B1

## Sommaire

- [TP1 : Les premiers pas de bébé B1](#tp1--les-premiers-pas-de-bébé-b1)
  - [Sommaire](#sommaire)
- [I. Récolte d'informations](#i-récolte-dinformations)
- [II. Utiliser le réseau](#ii-utiliser-le-réseau)
- [III. Sniffer le réseau](#iii-sniffer-le-réseau)
- [IV. Network scanning et adresses IP](#iv-network-scanning-et-adresses-ip)

# I. Récolte d'informations

**🌞 Adresses IP de ta machine**
```powershell
PS C:\Users\souri> ipconfig /all
Carte réseau sans fil Wi-Fi :

   Description. . . . . . . . . . . . . . : Intel(R) Wi-Fi 6E AX211 160MHz
   Adresse physique . . . . . . . . . . . : E4-0D-36-2F-88-9D
   Adresse IPv6 de liaison locale. . . . .: fe80::de61:f1c2:516a:9434%9(préféré)
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.78.252(préféré)

Carte Ethernet Ethernet :

   Statut du média. . . . . . . . . . . . : Média déconnecté
   Suffixe DNS propre à la connexion. . . : home
   Description. . . . . . . . . . . . . . : Realtek PCIe GbE Family Controller
   Adresse physique . . . . . . . . . . . : D4-93-90-31-58-D3
```

**🌞 Si t'as un accès internet normal, d'autres infos sont forcément dispos...**
```powershell
PS C:\Users\souri> ipconfig /all
Carte réseau sans fil Wi-Fi :

   Masque de sous-réseau. . . . . . . . . : 255.255.240.0
   Passerelle par défaut. . . . . . . . . : 10.33.79.254
   Serveur DHCP . . . . . . . . . . . . . : 10.33.79.254
   Serveurs DNS. . .  . . . . . . . . . . : 1.1.1.1
                                       1.0.0.1
```

**🌟 BONUS : Détermine s'il y a un pare-feu actif sur ta machine**
```powershell
PS C:\Users\souri> Get-NetFirewallProfile | ft Name,Enabled

Name    Enabled
----    -------
Domain     True
Private    True
Public     True

```
**🌟 Liste des règles du pare-feu**
```powershell
PS C:\Windows\system32> Show-NetFirewallRule

Name                          : SNMPTRAP-In-UDP
DisplayName                   : Service d’interruption SNMP (UDP entrant)
Description                   : Règle de trafic entrant pour que le service d’interruption SNMP autorise les interruptions SNMP. [UDP 162]
DisplayGroup                  : Interruption SNMP
Group                         : @firewallapi.dll,-50323
Enabled                       : False
Profile                       : Private, Public
Platform                      :
Direction                     : Inbound
Action                        : Allow
EdgeTraversalPolicy           : Block
LooseSourceMapping            : False
LocalOnlyMapping              : False
Owner                         :
PrimaryStatus                 : OK
Status                        : La règle a été analysée à partir de la banque. (65536)
EnforcementStatus             : NotApplicable
PolicyStoreSource             : PersistentStore
PolicyStoreSourceType         : Local
RemoteDynamicKeywordAddresses :
PolicyAppId                   :

$_ | Get-NetFirewallAddressFilter
     LocalAddress             : Any
     RemoteAddress            : LocalSubnet

$_ | Get-NetFirewallServiceFilter
     Service                  : SNMPTRAP

$_ | Get-NetFirewallApplicationFilter
     Program                  : %SystemRoot%\system32\snmptrap.exe
     Package                  :

$_ | Get-NetFirewallInterfaceFilter
     InterfaceAlias           : Any

$_ | Get-NetFirewallInterfaceTypeFilter
     InterfaceType            : Any

$_ | Get-NetFirewallPortFilter
     Protocol                 : UDP
     LocalPort                : 162
     RemotePort               : Any
     IcmpType                 : Any
     DynamicTarget            : Any

$_ | Get-NetFirewallSecurityFilter
     Authentication           : NotRequired
     Encryption               : NotRequired
     OverrideBlockRules       : False
     LocalUser                : Any
     RemoteUser               : Any
     RemoteMachine            : Any

[...]
```
# II. Utiliser le réseau
**🌞 Envoie un ping vers...**

```powershell
PS C:\Users\souri> ping 10.33.78.252

Envoi d’une requête 'Ping'  10.33.78.252 avec 32 octets de données :
Réponse de 10.33.78.252 : octets=32 temps<1ms TTL=128
Réponse de 10.33.78.252 : octets=32 temps<1ms TTL=128
Réponse de 10.33.78.252 : octets=32 temps<1ms TTL=128
Réponse de 10.33.78.252 : octets=32 temps<1ms TTL=128

Statistiques Ping pour 10.33.78.252:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 0ms, Moyenne = 0ms
```
```powershell
PS C:\Users\souri> ping 127.0.0.1

Envoi d’une requête 'Ping'  127.0.0.1 avec 32 octets de données :
Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128
Réponse de 127.0.0.1 : octets=32 temps<1ms TTL=128

Statistiques Ping pour 127.0.0.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 0ms, Moyenne = 0ms
```

**🌞 On continue avec ping. Envoie un ping vers...**
- ta passerelle
```powershell
PS C:\Users\souri> ping 10.33.79.254

Envoi d’une requête 'Ping'  10.33.79.254 avec 32 octets de données :
Délai d’attente de la demande dépassé.
Délai d’attente de la demande dépassé.
Délai d’attente de la demande dépassé.
Délai d’attente de la demande dépassé.

Statistiques Ping pour 10.33.79.254:
    Paquets : envoyés = 4, reçus = 0, perdus = 4 (perte 100%),
```

- un(e) pote sur le réseau
```powershell
PS C:\Users\souri> ping 10.33.78.91

Envoi d’une requête 'Ping'  10.33.78.91 avec 32 octets de données :
Réponse de 10.33.78.91 : octets=32 temps=123 ms TTL=64
Réponse de 10.33.78.91 : octets=32 temps=16 ms TTL=64
Réponse de 10.33.78.91 : octets=32 temps=128 ms TTL=64
Réponse de 10.33.78.91 : octets=32 temps=40 ms TTL=64

Statistiques Ping pour 10.33.78.91:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 16ms, Maximum = 128ms, Moyenne = 76ms
```
- un site internet
```powershell
PS C:\Users\souri> ping www.thinkerview.com

Envoi d’une requête 'ping' sur www.thinkerview.com [188.114.97.6] avec 32 octets de données :
Réponse de 188.114.97.6 : octets=32 temps=19 ms TTL=55
Réponse de 188.114.97.6 : octets=32 temps=25 ms TTL=55
Réponse de 188.114.97.6 : octets=32 temps=17 ms TTL=55
Réponse de 188.114.97.6 : octets=32 temps=16 ms TTL=55

Statistiques Ping pour 188.114.97.6:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 16ms, Maximum = 25ms, Moyenne = 19ms
```

**🌞 Faire une requête DNS à la main**
```powershell
PS C:\Users\souri> nslookup www.thinkerview.com
Serveur :   one.one.one.one
Address:  1.1.1.1

Reponse ne faisant pas autorite :
Nom :    www.thinkerview.com
Addresses:  2a06:98c1:3120::6
          2a06:98c1:3121::6
          188.114.96.6
          188.114.97.6

PS C:\Users\souri> nslookup www.wikileaks.org
Serveur :   one.one.one.one
Address:  1.1.1.1

Reponse ne faisant pas autorite :
Nom :    wikileaks.org
Addresses:  80.81.248.21
          51.159.197.136
Aliases:  www.wikileaks.org

PS C:\Users\souri> nslookup www.torproject.org
Serveur :   one.one.one.one
Address:  1.1.1.1

Reponse ne faisant pas autorite :
Nom :    www.torproject.org
Addresses:  2620:7:6002:0:466:39ff:fe32:e3dd
          2620:7:6002:0:466:39ff:fe7f:1826
          2a01:4f8:fff0:4f:266:37ff:fe2c:5d19
          2a01:4f8:fff0:4f:266:37ff:feae:3bbc
          2a01:4f9:c010:19eb::1
          95.216.163.36
          116.202.120.165
          116.202.120.166
          204.8.99.144
          204.8.99.146
```
# III. Sniffer le réseau

[Fichier ip.pcap](ping.pcap)

[Fichier dns.pcap](dns.pcap)
# IV. Network scanning et adresses IP

**🌞 Effectue un scan du réseau auquel tu es connecté**
```powershell
PS C:\Users\souri> nmap -sn -PR 10.33.64.0/20
Starting Nmap 7.95 ( https://nmap.org ) at 2024-09-27 11:48 Paris, Madrid (heure d’ete)
Stats: 0:00:11 elapsed; 0 hosts completed (0 up), 4095 undergoing ARP Ping Scan
ARP Ping Scan Timing: About 10.74% done; ETC: 11:50 (0:01:31 remaining)
Stats: 0:00:33 elapsed; 0 hosts completed (0 up), 4095 undergoing ARP Ping Scan
ARP Ping Scan Timing: About 28.00% done; ETC: 11:50 (0:01:25 remaining)
Stats: 0:02:42 elapsed; 0 hosts completed (0 up), 4095 undergoing ARP Ping Scan
Parallel DNS resolution of 549 hosts. Timing: About 98.18% done; ETC: 11:51 (0:00:00 remaining)
Nmap scan report for 10.33.66.78
Host is up (0.083s latency).
MAC Address: E4:B3:18:48:36:68 (Intel Corporate)
Nmap scan report for 10.33.67.113
Host is up (0.036s latency).
MAC Address: D2:91:DE:DF:9A:6E (Unknown)
Nmap scan report for 10.33.69.68
Host is up (0.12s latency).
MAC Address: EE:E8:D9:89:3F:F1 (Unknown)
Nmap scan report for 10.33.69.89
Host is up (0.37s latency).
MAC Address: AC:C9:06:10:14:B6 (Apple)
Nmap scan report for 10.33.69.90
Host is up (0.033s latency).
MAC Address: 60:E9:AA:DD:EE:4D (Cloud Network Technology Singapore PTE.)
[...]
MAC Address: D8:80:83:D0:03:05 (Cloud Network Technology Singapore PTE.)
Nmap scan report for 10.33.79.254
Host is up (0.022s latency).
MAC Address: 7C:5A:1C:D3:D8:76 (Sophos)
Nmap scan report for 10.33.78.252
Host is up.
Nmap done: 4096 IP addresses (550 hosts up) scanned in 165.66 seconds
```
**🌞 Changer d'adresse IP**

```powershell
PS C:\Windows\system32> netsh interface ipv4 set address name="Wi-Fi" static 10.33.78.172

PS C:\Windows\system32> ipconfig /all

Carte réseau sans fil Wi-Fi :

   Description. . . . . . . . . . . . . . : Intel(R) Wi-Fi 6E AX211 160MHz
   Adresse physique . . . . . . . . . . . : E4-0D-36-2F-88-9D
   DHCP activé. . . . . . . . . . . . . . : Non
   Adresse IPv6 de liaison locale. . . . .: fe80::de61:f1c2:516a:9434%9(préféré)
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.78.172(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.0.0.0
   Serveurs DNS. . .  . . . . . . . . . . : 1.1.1.1
                                       1.0.0.1
   NetBIOS sur Tcpip. . . . . . . . . . . : Activé
```

(pour revenir sur une ip non statique: `netsh interface ipv4 set address name="Wi-Fi" source=dhcp`)