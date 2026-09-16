---
id: cvd-datacenter_ai-cisco-data-center-networking-blueprint-for-ai-ml-application
title: Cisco Data Center Networking Blueprint for AI/ML Applications
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/cisco-data-center-networking-blueprint-for-ai-ml-applications.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- ai
- applications
- blueprint
- center
- cisco
- cvd
- data
- datacenter_ai
- for
- ml
- networking
---
Fabric de IA con Nexus 9000 (hasta 25.6 Tbps por ASIC, ~1.5 µs de latencia); Nexus 9300 93600CD-GX y 9332D-GX2B para spine-leaf. Transporte sin pérdida con RoCEv2 (RDMA sobre Ethernet): ECN marca en umbral de cola y PFC aplica pausa por enlace; juntos implementan DCQCN. Ejemplo de dimensionamiento: clúster de 1024 GPUs con diez leaf 93600CD-GX (256×100G) a cuatro spine 9332D-GX2B (80×400G) = fabric no bloqueante. Nexus Dashboard Insights (telemetría) y Fabric Controller (QoS lossless).
