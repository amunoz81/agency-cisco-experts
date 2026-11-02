---
id: cvd-security-zero-trust-network-and-cloud-security-design-guide
title: 'Zero Trust: Network and Cloud Security Design Guide'
architecture: security
source: https://www.cisco.com/c/en/us/solutions/collateral/enterprise/design-zone-security/zt-network-cloud-dg.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- and
- cloud
- cvd
- design
- guide
- network
- security
- trust
- zero
---
Guía de diseño Zero Trust centrada en controles de red y nube para flujos de negocio típicos: empleado con dispositivo de confianza en sucursal accediendo a una aplicación privada, y acceso a Internet de invitados. Cisco ISE clasifica el tráfico con Scalable Group Tags (SGT) y los comparte con Secure Firewall vía pxGrid; SXP distribuye las etiquetas de destino entre switches (Catalyst 9300) y firewall cuando no hay inline tagging. Secure Network Analytics aporta telemetría NetFlow para detectar comportamiento anómalo y validar que la segmentación por SGT se cumple. El diseño aplica control de acceso basado en grupos (no en IP) en el límite entre segmentos de red y nube, reduciendo el movimiento lateral. Pensada para leerse junto con las guías Zero Trust: User and Device Security (usuario/dispositivo) y Secure Remote Worker On-Prem (VPN), formando el conjunto de guías Zero Trust de Cisco por capa: usuario/dispositivo, red/nube y acceso remoto.
