---
id: cvd-datacenter_ai-cisco-ai-pod-with-flashstack-for-secure-enterprise-ai-factor
title: Cisco AI POD with FlashStack for Secure Enterprise AI Factories Design Guide
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flashstack_aipod_secure_enterprise_ai_factories_design_guide.html
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- ai
- cisco
- cvd
- datacenter_ai
- design
- enterprise
- factories
- flashstack
- for
- guide
- pod
- secure
- with
---
Guía de diseño de Cisco AI PODs con FlashStack para AI Factories empresariales seguras, que detalla el nodo PCIe UCS X580p dentro del chassis modular X-Series. Cada X580p alberga hasta cuatro GPUs NVIDIA y se empareja con un nodo de cómputo X-Series para CPU/ memoria host; un chasis admite hasta dos nodos X580p (ocho GPUs en total), y los dos nodos del mismo chasis pueden usar modelos de GPU distintos, aunque dentro de un mismo nodo todas las GPUs deben ser del mismo modelo. El BOM valida RTX PRO 6000 Blackwell Server Edition y H200 NVL. Red backend con adaptadores NVIDIA ConnectX-7 en módulos X-Fabric X9516, con diseño de un enlace backend de 400 GbE por cada grupo de dos GPUs. Memoria de sistema recomendada: al menos 3 veces la memoria combinada de las GPUs asignadas al nodo. Escalabilidad: los Fabric Interconnects soportan hasta 20 chasis UCS X9508, para un máximo de plataforma de 160 GPUs. Se integra con almacenamiento FlashStack (Pure Storage) para datasets de entrenamiento/inferencia.
