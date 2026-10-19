---
id: cvd-datacenter_ai-cisco-massively-scalable-data-center-network-fabric-white-pa
title: Cisco Massively Scalable Data Center Network Fabric White Paper
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-743245.html
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- center
- cisco
- cvd
- data
- datacenter_ai
- fabric
- massively
- network
- paper
- scalable
- white
---
Guía de diseño de fabrics Clos de gran escala sobre Nexus 9000. El bloque de construcción básico es el server pod: una topología spine-leaf de dos niveles donde cada leaf se conecta en malla completa a cada spine del pod; escalar horizontalmente significa agregar más server pods. Documenta cuatro ejemplos de diseño, incluido el fabric clásico de tres niveles (spine-leaf) y un ejemplo específico para redes de IA con esquema de "rail and plane". Se complementa con el enfoque VXLAN BGP EVPN, que contrasta el fabric Clos de 3 etapas (leaf-spine) con la variante de 5 etapas, que añade una capa de super-spine para interconectar spines entre localidades o pods. Sirve como referencia de dimensionamiento para fabrics de datacenter e IA de muy alta escala, más allá de un solo par spine-leaf.
