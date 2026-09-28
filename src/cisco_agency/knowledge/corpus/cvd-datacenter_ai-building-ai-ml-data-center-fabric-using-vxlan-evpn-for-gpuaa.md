---
id: cvd-datacenter_ai-building-ai-ml-data-center-fabric-using-vxlan-evpn-for-gpuaa
title: Building AI/ML Data Center Fabric using VXLAN EVPN for GPUaaS
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/building-aiml-dc-fabric-using-vxlan-evpn-for-gpuaas.html
source_date: '2026-09-28'
version: '2026'
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
Guía de diseño para construir un fabric spine-leaf VXLAN BGP EVPN dedicado a ofrecer GPU-as-a-Service (GPUaaS) multi-tenant. Se basa en servidores densos de GPU Cisco UCS C885A M8 conectados a switches Nexus 9000 (incluye el Nexus 9364D-GX2A, 2RU con 64 puertos QSFP-DD de 400G y hasta 25.6 Tbps de capacidad de conmutación a line-rate) organizados en topología leaf-spine. El overlay VXLAN EVPN provee dominios Capa 2 aislados y seguros por cliente/tenant, de modo que cada consumidor de GPUaaS opera sin tráfico cruzado entre tenants sobre una infraestructura física compartida. Nexus Dashboard aporta automatización basada en intención, gestión centralizada y visibilidad extremo a extremo del fabric, con una guía paso a paso para configurar el fabric spine-leaf optimizado para AI/ML. Incluye ejemplos de configuración, casos de uso y procedimientos de despliegue completos: referencia de diseño multi-tenant complementaria al fabric de IA no bloqueante ya cubierto para clústeres GPU de un solo tenant.
