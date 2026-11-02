---
id: cvd-secure_networking-cisco-software-defined-access-sd-access-design-guide-cvd
title: Cisco Software-Defined Access (SD-Access) Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-sda-design-guide.html
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- access
- cisco
- cvd
- defined
- design
- guide
- sd
- secure_networking
- software
---
Guía de diseño validada de SD-Access: fabric de campus con plano de overlay (LISP para control, VXLAN para datos), underlay enrutado y plano de política (Cisco Catalyst Center como motor de automatización y Scalable Group Tags para segmentación por intención). Catalyst Center aprovisiona el underlay y automatiza los roles del fabric: edge (acceso), border (conectividad externa/L3), control plane node (resolución de endpoints) e intermediate. Wireless integrado en modo fabric con APs Catalyst y controladores embebidos o Catalyst 9800. Define modelos de referencia por tamaño de sitio (fabric en una caja para sitios pequeños, distribuido para campus grandes) y multisite para interconectar fabrics en distintas ubicaciones. La segmentación macro (Virtual Networks) y micro (SGT) sustituye a las VLANs tradicionales, habilitando políticas consistentes wired/wireless con aprovisionamiento centralizado.
