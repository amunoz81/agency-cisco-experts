---
id: cvd-observability_soc-cisco-event-agentic-socs-a-reference-architecture-operations
title: 'Cisco Event Agentic SOCs: A Reference Architecture & Operations Guide'
architecture: observability_soc
source: https://www.cisco.com/c/dam/en/us/products/collateral/security/cisco-event-socs.pdf
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- a
- agentic
- architecture
- cisco
- cvd
- event
- guide
- observability_soc
- operations
- reference
- socs
---
Guía de referencia y operación para montar un SOC temporal de alto rendimiento en eventos grandes (conferencias de varios días con miles de dispositivos), basada en la experiencia operativa de Cisco en sus propios eventos. Combina Cisco XDR como punto de triage rápido para analistas (incluyendo personal rotativo o junior) con Splunk Enterprise Security para la correlación y la investigación profunda de incidentes. La arquitectura de referencia se apoya en Cisco Cloud Control para gestión unificada, telemetría de seguridad de Cisco (red, endpoint, firewall), inteligencia de amenazas de Cisco Talos y captura continua de paquetes con Endace para forense posterior al incidente. El enfoque prioriza tiempos de despliegue y desmontaje muy cortos, visibilidad centralizada desde el primer minuto y un modelo de triage escalonado (XDR para alertas de alto volumen, Splunk ES para hunting y correlación cross-fuente). Útil como patrón de SOC efímero/pop-up, también aplicable a entornos empresariales que necesitan escalar capacidad de monitoreo de forma temporal.
