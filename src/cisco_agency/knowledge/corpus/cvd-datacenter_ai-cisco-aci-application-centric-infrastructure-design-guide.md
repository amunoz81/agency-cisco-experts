---
id: cvd-datacenter_ai-cisco-aci-application-centric-infrastructure-design-guide
title: Cisco ACI (Application Centric Infrastructure) Design Guide
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/cisco-application-centric-infrastructure-design-guide.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- aci
- application
- centric
- cisco
- cvd
- datacenter_ai
- design
- guide
- infrastructure
---
Topología spine-leaf (y multi-tier) con Nexus 9000 y APIC como controlador de política centralizado. Leaf = VTEP de conexión de cargas; spine = interconexión y mapeo endpoint-VTEP; APIC en clúster para redundancia. Construcciones: Tenants (partición), EPGs (segmentación por política), VRFs (routing multi-tenant), Contracts (política stateful entre EPGs). Prácticas: emparejar generaciones de HW en vPC, border leaf para L3 externo, versiones de SW consistentes en upgrades, dimensionar spines por escalabilidad de endpoints, aplicar política en ingress de VRF.
