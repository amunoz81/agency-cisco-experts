---
id: cvd-datacenter_ai-building-ai-ml-data-center-fabric-using-vxlan-evpn-for-gpuaa
title: Building AI/ML Data Center Fabric using VXLAN EVPN for GPUaaS
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/building-aiml-dc-fabric-using-vxlan-evpn-for-gpuaas.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- ai
- building
- center
- cvd
- data
- datacenter_ai
- evpn
- fabric
- for
- gpuaas
- ml
- using
- vxlan
---
Blueprint de Cisco para construir fabrics de datacenter para cargas de IA/ML mediante overlay VXLAN EVPN, basado en un despliegue real con servidores Cisco UCS C885A M8 densos en GPU y GPUs NVIDIA. La arquitectura de referencia usa switches Nexus 9364D-GX2A (64 puertos de 400GbE QSFP-DD, hasta 25.6 Tbps, ASIC SoC con 4 pares de slices) tanto en spine como en leaf -ejemplo con 16 spines y 24 leaves corriendo NX-OS 10.5(3)F-, con 16 puertos por par de slice alineados al cableado rail-optimized de clústeres de GPU para flujos de baja latencia y predecibles. Gestión y automatización con Cisco Nexus Dashboard 4.1, que reduce el tiempo de aprovisionamiento de días a horas. VXLAN EVPN aporta multi-tenencia segura, permitiendo segmentar de forma aislada entornos de investigación, producción y desarrollo de IA sobre la misma infraestructura física, con ancho de banda predecible y line-rate en todos los puertos.
