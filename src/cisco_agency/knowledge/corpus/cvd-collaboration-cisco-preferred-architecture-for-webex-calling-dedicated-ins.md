---
id: cvd-collaboration-cisco-preferred-architecture-for-webex-calling-dedicated-ins
title: Cisco Preferred Architecture for Webex Calling Dedicated Instance
architecture: collaboration
source: https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/hybrid/AltDesigns/PA-WbxCallDI.pdf
source_date: '2026-09-15'
version: sep 2025
status: verificada
tags:
- architecture
- calling
- cisco
- collaboration
- cvd
- dedicated
- for
- instance
- preferred
- webex
---
Arquitectura preferida para Webex Calling Dedicated Instance (DI): entorno UC dedicado en la nube que combina las funcionalidades tradicionales de Unified CM con los beneficios de la plataforma Webex. Dimensionamiento: un clúster DI completamente desplegado soporta hasta 8 servidores de procesamiento de llamadas y aproximadamente 50,000 dispositivos (versión 14 y posteriores). Opciones de conectividad PSTN: Cloud Connected PSTN (CCP, aprovechando el peering existente de partners CCP con Webex Calling), Local Gateway (que termina un troncal TDM/IP en el mismo router o se conecta vía SIP trunk a un gateway PSTN existente, usando un Cisco Unified Border Element -CUBE- o voice gateway), y Local Gateway hosteado por un partner en su propio datacenter. Prácticas recomendadas: troncales SIP seguros entre Unified CM y el gateway o CUBE para llamadas salientes a PSTN, con TLS para cifrado de señalización y SRTP para cifrado de medios.
