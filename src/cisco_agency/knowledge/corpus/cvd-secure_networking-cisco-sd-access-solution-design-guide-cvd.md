---
id: cvd-secure_networking-cisco-sd-access-solution-design-guide-cvd
title: Cisco SD-Access Solution Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-sda-design-guide.html
source_date: '2026-09-15'
version: '2025'
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
Guía de diseño de Cisco Software-Defined Access (SD-Access), la solución de fabric para campus orquestada por Catalyst Center. Separa tres planos: control (LISP, con Map-Server/Map-Resolver que rastrea endpoints y los asocia al RLOC del edge node), datos (VXLAN para el overlay) y política (TrustSec con SGT). Roles de fabric: edge node (conexión de endpoints y registro en el control plane), border node (externo como gateway de último recurso hacia fuera del fabric; interno para registrar subredes conocidas) y control plane node. El underlay se aprovisiona típicamente con IS-IS vía LAN Automation; el overlay se construye encima sin que el tráfico de cliente use el underlay. En sitios pequeños los tres roles pueden colapsarse en un mismo dispositivo; en diseños de alta disponibilidad, border y control plane suelen colocarse en un par redundante de core con enlace cruzado. El diseño multisitio enlaza fabrics mediante señalización LISP y encapsulación VXLAN, con rutas de underlay conocidas entre los loopbacks de los border nodes.
