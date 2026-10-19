---
id: cvd-security-cisco-secure-firewall-threat-defense-sd-wan-design-and-deplo
title: Cisco Secure Firewall Threat Defense SD-WAN Design and Deployment Guide
architecture: security
source: https://www.cisco.com/c/en/us/td/docs/security/secure-firewall/cvd/secure-firewall-sdwan-deployment-guide.html
source_date: '2026-09-15'
version: '7.6'
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
- security
- threat
- wan
---
Guía de diseño y despliegue de SD-WAN con Cisco Secure Firewall Threat Defense y Firewall Management Center (release 7.6), complementaria al SASE/SSE del catálogo. Arquitectura hub-and-spoke con túneles VTI enrutados: el hub usa una Dynamic VTI (DVTI) que crea una interfaz virtual-access por spoke desde una plantilla, mientras cada spoke usa una Static VTI (SVTI) unidireccional para iniciar el túnel. BGP, OSPF o EIGRP corren sobre el overlay; el asistente de Management Center automatiza DVTIs/SVTIs y el BGP del overlay. Los hubs retransmiten tráfico spoke-to-spoke (los spokes no se comunican directo entre sí). Soporta hasta dos hubs por topología y hasta 1024 interfaces de túnel virtual; dual hub/dual ISP produce 16 túneles. Policy-Based Routing con monitoreo de ruta (sondas ICMP, probe HTTP de 10s) habilita Direct Internet Access; ECMP agrega ancho de banda entre ISPs/VTIs. Redundancia hacia Cisco Secure Access vía hub primario/ secundario y túneles activo-activo/activo-backup (hasta 16 túneles, 1 Gbps cada uno). Cisco recomienda un solo hub en topologías route-based simples.
