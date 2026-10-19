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
Arquitectura preferida de Cisco para Webex Calling Dedicated Instance (DI), la variante de Unified CM gestionada en nube dedicada por cliente, complementaria al Webex Calling multi-tenant del catálogo. Un clúster consiste en un nodo publisher y múltiples subscribers; un clúster DI completamente desplegado soporta hasta 8 servidores de call processing o ~50,000 dispositivos (versión 14+). El número de Knowledge Workers y dispositivos de Common Area capturado durante la activación del servicio determina si se requieren múltiples clústeres DI en una misma región. Mixed mode viene habilitado por defecto (el comportamiento depende del endpoint). SIP OAuth (introducido en Unified CM 12.5(1)+) puede operar con o sin mixed mode; mixed mode sigue siendo necesario para cifrado entre clientes Webex y otros dispositivos Unified CM que no soportan SIP OAuth. Hybrid Calling for Devices (device connector) no es soportado dentro de DI. Base para dimensionar clústeres DI por usuario/dispositivo y decidir la topología multi-clúster por región.
