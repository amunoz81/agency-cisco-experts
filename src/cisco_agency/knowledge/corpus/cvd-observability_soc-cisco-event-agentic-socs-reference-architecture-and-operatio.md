---
id: cvd-observability_soc-cisco-event-agentic-socs-reference-architecture-and-operatio
title: 'Cisco Event Agentic SOCs: Reference Architecture and Operations Guide'
architecture: observability_soc
source: https://www.cisco.com/c/dam/en/us/products/collateral/security/cisco-event-socs.pdf
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- agentic
- and
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
Framework de referencia repetible de Cisco para construir y operar SOCs agénticos ("Agentic SOC") en eventos grandes y de corta duración (p. ej. RSAC, Cisco Live, Black Hat), basado en despliegues reales en dichos eventos. Arquitectura "SOC in a Box": Splunk Enterprise Security como plano único de análisis y registro canónico de incidentes, integrado con Cisco XDR (recolección/procesamiento de telemetría, SOAR con playbooks y conector de sistemas), Cisco Secure Firewall (enforcement inline), Cisco Secure Access (seguridad DNS), Endace (captura continua de paquetes para investigación forense), Secure Network Analytics, ThousandEyes, Splunk Attack Analyzer, Secure Malware Analytics y Talos. XDR detecta cambios de escalamiento y los transforma en investigaciones estructuradas de Splunk ES, generando hallazgos y entidades de riesgo. Modelo operativo human-in-the-loop: los agentes de IA resumen y recomiendan, pero los analistas validan y deciden la respuesta final.
