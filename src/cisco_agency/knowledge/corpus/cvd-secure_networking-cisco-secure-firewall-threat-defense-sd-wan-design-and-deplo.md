---
id: cvd-secure_networking-cisco-secure-firewall-threat-defense-sd-wan-design-and-deplo
title: Cisco Secure Firewall Threat Defense SD-WAN Design and Deployment Guide
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/security/secure-firewall/cvd/secure-firewall-sdwan-deployment-guide.html
source_date: '2026-09-28'
version: '2026'
status: verificada
tags:
- and
- cisco
- cvd
- defense
- deployment
- design
- firewall
- guide
- sd
- secure
- secure_networking
- threat
- wan
---
Guía de diseño para desplegar Cisco Secure Firewall Threat Defense (FTD), gestionado por Secure Firewall Management Center, como firewall de rama integrado en una arquitectura SD-WAN altamente disponible. Usa Virtual Tunnel Interfaces (VTI), interfaces lógicas enrutables sobre las que se aplican políticas de enrutamiento estático o dinámico (BGP) para anunciar alcanzabilidad hacia los hubs. Para Secure Internet Access (SIA) en rama, la alta disponibilidad se logra con IKE Dead Peer Detection (DPD) en enrutamiento estático (el túnel conmuta automáticamente al hub secundario si el par primario deja de responder) o con failover de sesiones BGP en enrutamiento dinámico (el FTD pivota al siguiente par BGP si cae el path primario), asegurando acceso a Internet continuo ante fallas de componente o de datacenter. Integra IPS, filtrado de URL y demás inspecciones de Threat Defense como base de seguridad en el borde de la rama, combinando firewall de próxima generación y conectividad SD-WAN en un dispositivo gestionado centralmente.
