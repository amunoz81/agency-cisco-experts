---
id: cvd-secure_networking-cisco-secure-networking-sd-access-deployment-guide
title: Cisco Secure Networking SD-Access Deployment Guide
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/Cisco-Secure-Networking-SD-Access-Deployment-Guide.html
source_date: '2026-09-15'
version: oct 2026
status: verificada
tags:
- access
- cisco
- cvd
- deployment
- guide
- networking
- sd
- secure
- secure_networking
---
Guía de despliegue validada para un fabric SD-Access de campus de escala media en un único sitio, construida sobre la Cisco Secure Network Reference Architecture y orquestada con Catalyst Center. Underlay enrutado con OSPF aprovisionado por LAN Automation; overlay LISP/VXLAN con macro-segmentación basada en VRF y micro-segmentación con Cisco ISE y TrustSec (SGT) para política consistente wired/wireless. Línea base validada: IOS XE 17.18.2 en nodos de fabric, fusion y controladoras wireless, con Catalyst Center en la rama 3.x. Cubre planeación del despliegue, conectividad cableada e inalámbrica, integraciones de seguridad (ISE/TrustSec) y validación del diseño. Las fabric zones son obligatorias en sitios de gran escala para limitar el dominio de fallas, con un máximo de dispositivos de fabric por zona según el appliance de Catalyst Center. Referencia para clientes que requieren segmentación de identidad y aplicación de política de seguridad integradas directamente en la arquitectura de campus, no solo como una capa superpuesta.
