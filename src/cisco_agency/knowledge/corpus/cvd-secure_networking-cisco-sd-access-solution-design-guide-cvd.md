---
id: cvd-secure_networking-cisco-sd-access-solution-design-guide-cvd
title: Cisco SD-Access Solution Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-sda-design-guide.html
source_date: '2026-09-28'
version: '2026'
status: verificada
tags:
- access
- cisco
- cvd
- design
- guide
- sd
- secure_networking
- solution
---
Guía de diseño de Software-Defined Access (SD-Access) sobre fabric de campus con Cisco Catalyst Center como controlador de automatización e intención. Tres roles de nodo: edge (equivalente a la capa de acceso, basado en xTR de LISP), control-plane (implementa LISP Map-Server/ Map-Resolver y mantiene la base de host-tracking con el binding EID-a-RLOC de cada endpoint) y border (punto de entrada/salida hacia redes externas al fabric). El overlay extiende conectividad de Capa 2 y Capa 3 mediante LISP (plano de control) y VXLAN (plano de datos), desacoplando la identidad del endpoint de su ubicación topológica. Recomienda nodos de control-plane redundantes del mismo tipo de plataforma para desempeño consistente, ya que border y edge nodes se registran contra todos los nodos de control-plane disponibles. Habilita macro-segmentación por Virtual Network (VN) y micro-segmentación por Scalable Group Tag (SGT/TrustSec) aplicada de forma consistente en wired y wireless, como alternativa basada en intención al diseño LAN/WLAN tradicional de Catalyst 9000.
