# TP4 : DHCP et accès internet

## Sommaire

- [TP4 : DHCP et accès internet](#tp4--dhcp-et-accès-internet)
  - [Sommaire](#sommaire)
- [I. DHCP](#i-dhcp)
  - [1. Les mains dans le capot](#1-les-mains-dans-le-capot)

## 1. Les mains dans le capot

☀️ **Capturez un échange DHCP complet**

[Fichier dhcp.pcap](dhcp.pcap)

☀️ **Directement dans Wireshark, vous pouvez voir toutes les infos que vous donne  le serveur DHCP**

- adresse IP proposée
```powershell
Your (client) IP address: 10.33.78.252
```
- serveur DNS indiqué
```powershell
Option(6) Domain Name Server: 8.8.8.8, 1.1.1.1
```

- passerelle du réseau
```powershell
Option(54) DHCP Server Identifier (10.33.79.254)
```