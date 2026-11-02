---
id: cvd-datacenter_ai-building-ai-ml-data-center-fabric-using-vxlan-evpn-for-gpuaa
title: Building AI/ML Data Center Fabric using VXLAN EVPN for GPUaaS
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/building-aiml-dc-fabric-using-vxlan-evpn-for-gpuaas.html
source_date: '2026-09-15'
version: mar 2026
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
Whitepaper técnico sobre cómo construir un fabric de datacenter para IA/ML multi-tenant usando VXLAN BGP EVPN sobre switches Nexus 9000, pensado para escenarios de GPU-as-a-Service donde varios clientes comparten la misma infraestructura física de GPUs de forma aislada. Describe un blueprint no bloqueante (non-blocking) validado por Cisco, configurado y operado desde Cisco Nexus Dashboard, que recomienda las plantillas de fabric eBGP Routed o VXLAN EVPN Fabric como las más adecuadas para construir fabrics de IA/ML dentro de Nexus Dashboard. El aislamiento multi-tenant se logra con los mismos constructos EVPN del resto del catálogo (VRFs y VNIs por tenant), orientados a separar clústeres de GPU de distintos clientes sobre un mismo fabric físico. Complementa la guía genérica VXLAN BGP EVPN Design and Implementation Guide y el Data Center Networking Blueprint for AI/ML Applications ya presentes en el catálogo, enfocándose en el caso de uso comercial de revender capacidad de GPU como servicio.
