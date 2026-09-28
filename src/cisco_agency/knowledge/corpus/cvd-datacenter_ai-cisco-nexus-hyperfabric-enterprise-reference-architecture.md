---
id: cvd-datacenter_ai-cisco-nexus-hyperfabric-enterprise-reference-architecture
title: Cisco Nexus Hyperfabric Enterprise Reference Architecture
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/products/collateral/data-center-networking/nexus-hyperfabric/hyperfabric-ai-era-ds.html
source_date: '2026-09-28'
version: '2026'
status: verificada
tags:
- architecture
- cisco
- cvd
- datacenter_ai
- enterprise
- hyperfabric
- nexus
- reference
---
Arquitectura de referencia full-stack para infraestructura de IA on-premises, gestionada por un controlador Cisco Nexus Hyperfabric alojado en la nube y alineada con la NVIDIA Enterprise Reference Architecture para NVIDIA HGX H200 y la red NVIDIA Spectrum-X. Cómputo con el servidor Cisco UCS C885A M8 (8RU, alta densidad de GPU) para entrenamiento, fine-tuning, inferencia de modelos grandes y RAG. Red con el switch Cisco N9164E-NS4-O, basado en NPU NVIDIA Spectrum-4 (2RU, hasta 64 puertos 800G OSFP o 128 puertos 400GE), utilizable en rol leaf o spine de la red este-oeste de cómputo. La tecnología NVIDIA Spectrum-X mejora el rendimiento y eficiencia de redes Ethernet para GPU y storage; sus beneficios se obtienen con switches Hyperfabric basados en Cisco Silicon One conectados a SuperNICs NVIDIA BlueField-3 con la licencia Fine Grain Load Balancing (FGLB) habilitada. El controlador cloud gestiona diseño, pedido, despliegue, operación y escalado del fabric, GPUs, storage y red como una sola unidad de infraestructura de IA.
