# TP2 : Hey yo tell a neighbor tell a friend

# Sommaire

- [TP2 : Hey yo tell a neighbor tell a friend](#tp2--hey-yo-tell-a-neighbor-tell-a-friend)
- [Sommaire](#sommaire)
- [I. Simplest LAN](#i-simplest-lan)
  - [1. Quelques pings](#1-quelques-pings)
- [II. Utilisation des ports](#ii-utilisation-des-ports)
  - [1. Animal numérique](#1-animal-numérique)
- [III. Analyse de vos applications usuelles](#iii-analyse-de-vos-applications-usuelles)
  - [1. Serveur web](#1-serveur-web)
  - [2. Autres services](#2-autres-services)


# I. Simplest LAN

## 1. Quelques pings

**🌞 Prouvez que votre configuration est effective**

```powershell
PS C:\Windows\system32> Get-NetIPAddress -InterfaceAlias Ethernet

IPAddress         : fe80::a124:456e:7d26:898a%2
InterfaceIndex    : 2
InterfaceAlias    : Ethernet
AddressFamily     : IPv6
Type              : Unicast
PrefixLength      : 64
PrefixOrigin      : WellKnown
SuffixOrigin      : Link
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore

IPAddress         : 10.1.1.1
InterfaceIndex    : 2
InterfaceAlias    : Ethernet
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 24
PrefixOrigin      : Manual
SuffixOrigin      : Manual
AddressState      : Preferred
ValidLifetime     : Infinite ([TimeSpan]::MaxValue)
PreferredLifetime : Infinite ([TimeSpan]::MaxValue)
SkipAsSource      : False
PolicyStore       : ActiveStore
```

**🌞 Tester que votre LAN + votre adressage IP est fonctionnel**

```powershell
PS C:\Windows\system32> ping 10.33.66.78

Envoi d’une requête 'Ping'  10.33.66.78 avec 32 octets de données :
Réponse de 10.33.66.78 : octets=32 temps=74 ms TTL=64
Réponse de 10.33.66.78 : octets=32 temps=91 ms TTL=64
Réponse de 10.33.66.78 : octets=32 temps=98 ms TTL=64
Réponse de 10.33.66.78 : octets=32 temps=106 ms TTL=64

Statistiques Ping pour 10.33.66.78:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 74ms, Maximum = 106ms, Moyenne = 92ms
```

**🌞 Capture de ping**

[Fichier ping.pcap](ping.pcap)

# II. Utilisation des ports

## 1. Animal numérique

**🌞 Sur le PC serveur**

```powershell
PS C:\Windows\system32> nc -lnvp 9999
listening on [any] 9999 ...
```

**🌞 Sur le PC serveur toujours**
```powershell
PS C:\Windows\system32> netstat -a -b -n | Select-String 9999

  TCP    0.0.0.0:9999           0.0.0.0:0              LISTENING

```

**🌞 Sur le PC client**

```powershell
PS C:\Windows\system32> nc 10.1.1.1 9999
```

**🌞 Echangez-vous des messages**

```powershell
PS C:\Windows\system32> nc -lnvp 9999
listening on [any] 9999 ...
connect to [10.1.1.1] from (UNKNOWN) [10.1.1.2] 28502
salut
salut
```

**🌞 Utilisez une commande qui permet de voir la connexion en cours**

```powershell
PS C:\Windows\system32> netstat -a -b -n | Select-String 9999

  TCP    10.1.1.1:9999          10.1.1.2:28651         ESTABLISHED
```

**🌞 Faites une capture Wireshark complète d'un échange**

[Fichier netcat1.pcap](netcat1.pcap)

**🌞 Inversez les rôles**

```powershell
PS C:\Windows\system32> nc 10.1.1.2 9999
salut
wsh
cidsvpfxdv
vdbmd
```

```powershell
PS C:\Windows\system32> netstat -a -b -n | Select-String 9999

  TCP    10.1.1.1:54498         10.1.1.2:9999          ESTABLISHED
```

[Fichier netcat2.pcap](netcat2.pcap)

# III. Analyse de vos applications usuelles

## 1. Serveur web

**🌞 Utilisez Wireshark pour capturer du trafic HTTP**

[Fichier serverweb.pcap](serverweb.pcap)

## 2. Autres services

**🌞 Pour les 5 applications**

- Site web: (https://youtube.com)
  - [Capture](service1.pcap)
- Spotify
  - [Capture](service2.pcap)
- Steam
  - [Capture](service3.pcap)
- Discord
  - [Capture](service4.pcap)
- Anki
  - [Capture](service5.pcap)
