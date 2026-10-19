---
id: cvd-security-performance-and-scalability-guide-for-cisco-identity-service
title: Performance and Scalability Guide for Cisco Identity Services Engine (ISE)
architecture: security
source: https://www.cisco.com/c/en/us/td/docs/security/ise/performance_and_scalability/b_ise_perf_and_scale.html
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- and
- cisco
- cvd
- engine
- for
- guide
- identity
- ise
- performance
- scalability
- security
- services
---
Guía de dimensionamiento y arquitectura de despliegue de Cisco ISE (Policy Administration Node, Policy Service Node/PSN y Monitoring Node). Define tres tamaños de despliegue: pequeño (hasta 50,000 sesiones concurrentes activas), mediano (hasta 150,000) y grande (más de 150,000, con soporte de hasta 50 PSNs). Recomienda agrupar PSNs por tipo de carga de trabajo y repartir autenticaciones con balanceadores de carga, usando stickiness por Calling Station ID (dirección MAC) para mejorar el rendimiento de sesión. Para resiliencia, sugiere redundancia N+1 o N+2 dentro de cada grupo de PSNs, de forma que la pérdida de un nodo no sature al resto del grupo. Es la referencia para justificar el número de nodos ISE, su distribución geográfica y la capacidad de autenticación 802.1X/MAB requerida por el proyecto (campus, sucursal o acceso OT vía TrustSec).
