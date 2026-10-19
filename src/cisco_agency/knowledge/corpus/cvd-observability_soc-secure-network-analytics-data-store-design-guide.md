---
id: cvd-observability_soc-secure-network-analytics-data-store-design-guide
title: Secure Network Analytics Data Store Design Guide
architecture: observability_soc
source: https://www.cisco.com/c/dam/en/us/products/collateral/security/stealthwatch/stealthwatch-data-store-guide.pdf
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- analytics
- cvd
- data
- design
- guide
- network
- observability_soc
- secure
- store
---
Guía de diseño del Data Store de Cisco Secure Network Analytics (ex-Stealthwatch), la capa de almacenamiento distribuido entre el Manager y los Flow Collectors para analítica de NetFlow/telemetría a gran escala en el SOC. Los Flow Collectors envían telemetría a los Data Nodes para almacenamiento centralizado. Soporta diseños de un nodo o multi-nodo; un despliegue de un solo nodo no ofrece resiliencia de datos, y clústeres de dos nodos no son soportados (mínimo tres para redundancia real). Los Data Nodes de un mismo clúster deben ser homogéneos: todos hardware o todos Virtual Edition, sin mezclar. Modos de despliegue: Data Store, no-Data Store e híbrido (algunos Flow Collectors envían al Data Store y otros almacenan localmente). Recomienda un par redundante de switches interconectados que extiendan la misma VLAN L2 a ambos nodos de red; el Data Store no debe estirarse entre dos datacenters por la latencia entre Data Nodes. La función de Analytics (detección de anomalías) requiere una implementación Data Store (virtual o hardware) con cualquier número de Flow Collectors.
