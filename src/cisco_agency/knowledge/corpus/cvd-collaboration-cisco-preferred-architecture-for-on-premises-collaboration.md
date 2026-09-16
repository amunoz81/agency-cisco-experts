---
id: cvd-collaboration-cisco-preferred-architecture-for-on-premises-collaboration
title: Cisco Preferred Architecture for On-Premises Collaboration
architecture: collaboration
source: https://www.cisco.com/c/dam/en/us/td/docs/solutions/PA/overview/15x/clbpa15x.pdf
source_date: '2026-09-15'
version: 15.x
status: verificada
tags:
- architecture
- cisco
- collaboration
- cvd
- for
- 'on'
- preferred
- premises
---
Control de llamadas con Unified CM (registro de endpoints y enrutamiento) en clúster para redundancia. Expressway como borde (acceso remoto seguro y conectividad híbrida/nube) en pares HA; MRA para acceso externo sin VPN. CUBE como gateway PSTN (negociación de codecs y traducción de protocolo). Unity (mensajería unificada), IM&P (mensajería y presencia) y endpoints. Prácticas: redundancia geográfica, segregar voz/datos, monitoreo con RTMT, hardening (reglas de firewall, gestión de credenciales, parcheo regular).
