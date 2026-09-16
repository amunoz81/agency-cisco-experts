---
id: cvd-secure_networking-cisco-catalyst-sd-wan-design-guide-cvd
title: Cisco Catalyst SD-WAN Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- catalyst
- cisco
- cvd
- design
- guide
- sd
- secure_networking
- wan
---
Cuatro planos: orquestación (SD-WAN Validator/NAT traversal), gestión (SD-WAN Manager), control (SD-WAN Controllers) y datos (WAN Edge). Segmentación con VPNs: VPN 0 transporte, VPN 512 gestión OOB, VPNs 1-511 de servicio para datos. Cifrado AES-256 GCM con anti-replay (ventanas 64-4096; 4096 recomendado con QoS). OMP distribuye rutas, políticas y llaves por DTLS/TLS. Application-aware routing con SLA por sondas BFD (pérdida/latencia/jitter). Buenas prácticas: controladores redundantes por transporte, autenticación por certificados y lista de equipos autorizados, aprovisionamiento ZTP/PnP y segmentación por VPNs.
