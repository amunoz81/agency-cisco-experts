---
id: cvd-secure_networking-campus-lan-and-wlan-design-guide-cvd
title: Campus LAN and WLAN Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-campus-lan-wlan-design-guide.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- and
- campus
- cvd
- design
- guide
- lan
- secure_networking
- wlan
---
Catalyst 9000 en todo el diseño: acceso (9200/9300, 9400 modular), distribución (9400/9500/9600) y core (9500/9600). Wireless con Catalyst 9800 (appliance/virtual/embebido, 250-6000 APs) y APs Catalyst 9100 Wi-Fi 6. Recomienda capa de distribución simplificada con StackWise Virtual o stacks (uplinks activo-activo por EtherChannel, sin bloqueo STP). Segmentación avanzada con SD-Access (fabric overlay, políticas por intención wired/wireless) o BGP EVPN VXLAN (estándar abierto). Wireless en modo centralizado, FlexConnect o fabric SD-Access. Dimensionamiento: oversubscription acceso-distribución ~3.6:1, distribución-core ~4:1; mGig 2.5-5 Gbps y PoE+ (90-100W) para 802.11ax. Alta disponibilidad con SSO, NSF e ISSU para upgrades sin downtime.
