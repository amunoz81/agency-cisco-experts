---
id: cvd-observability_soc-deploying-cisco-aci-fabrics-with-telemetry-on-nexus-dashboar
title: Deploying Cisco ACI Fabrics with Telemetry on Nexus Dashboard
architecture: observability_soc
source: https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/getting-aci-ready-for-nd.html
source_date: '2026-09-28'
version: '2026'
status: verificada
tags:
- aci
- cisco
- cvd
- dashboard
- deploying
- fabrics
- nexus
- observability_soc
- 'on'
- telemetry
- with
---
White paper de diseño para instrumentar fabrics Cisco ACI con telemetría hacia Nexus Dashboard (base de Nexus Dashboard Insights). Desde ACI 6.1(2), la fuente de telemetría en APIC y switches puede configurarse por out-of-band (mgmt0) o in-band (SVI); en ambos casos la telemetría siempre se envía a las interfaces de datos de los nodos de Nexus Dashboard, nunca a sus puertos de gestión. Out-of-band es plug-and-play: reutiliza la red de gestión fuera de banda que ya existe para administración remota y recuperación ante desastres, sin configuración adicional. In-band, históricamente el único método disponible, requiere configurar bridge domains, EPGs, contracts y direcciones de gestión de nodo dentro del tenant mgmt, pero es la única opción que soporta Flow Telemetry y mayor ancho de banda de streaming. Recomienda revisar siempre la guía de despliegue de Nexus Dashboard específica de la versión antes de habilitar la telemetría; referencia clave para dimensionar la observabilidad de fabric que alimenta a Nexus Dashboard Insights.
