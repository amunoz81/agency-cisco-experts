---
id: cvd-secure_networking-cisco-sd-access-solution-design-guide-cvd
title: Cisco SD-Access Solution Design Guide (CVD)
architecture: secure_networking
source: https://www.cisco.com/c/en/us/td/docs/solutions/CVD/Campus/cisco-sda-design-guide.html
source_date: '2026-09-15'
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
Guía de diseño de la fabric SD-Access, gestionada por Cisco Catalyst Center. Define cuatro roles de nodo: control plane (base de mapeo endpoint-ubicación vía LISP, se recomiendan dos por redundancia), border (punto de entrada/salida del fabric; externo como gateway de último recurso con funcionalidad PxTR, o interno para redes conocidas como el datacenter), edge (donde se conectan endpoints y APs, colocados en la overlay INFRA_VN vía CDP) y nodos intermedios (core/distribución del underlay, tabla de ruteo global). El underlay es Layer 3 solo IPv4; la overlay encapsula tráfico de endpoints en VXLAN y puede ser IPv4 o dual stack. Modelos de sitio: Fabric in a Box (un stack/StackWise Virtual con los tres roles combinados, pensado para menos de 1000 endpoints) o sitios con control plane y border dedicados en pares redundantes; el handoff Layer 2 requiere un border dedicado, sin combinar roles.
