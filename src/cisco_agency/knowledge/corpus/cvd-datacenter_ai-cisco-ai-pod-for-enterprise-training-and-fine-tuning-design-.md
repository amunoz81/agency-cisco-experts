---
id: cvd-datacenter_ai-cisco-ai-pod-for-enterprise-training-and-fine-tuning-design-
title: Cisco AI POD for Enterprise Training and Fine-Tuning Design Guide
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/cisco_ai_pod_for_training_design.html
source_date: '2026-09-15'
version: ene 2026
status: verificada
tags:
- ai
- and
- cisco
- cvd
- datacenter_ai
- design
- enterprise
- fine
- for
- guide
- pod
- training
- tuning
---
Guía de diseño validada (CVD) para clústeres de entrenamiento y fine-tuning de IA empresarial con servidores GPU Cisco UCS C885A M8 y C845A M8, conectados a dos fabrics Nexus 9000 independientes: uno backend (este-oeste, tráfico GPU-a-GPU de alto ancho de banda) y uno frontend (norte-sur, acceso a almacenamiento y gestión), ambos administrados con Cisco Nexus Dashboard. Define puntos de partida modulares de 32, 64 y 128 GPUs, escalables en unidades, usando switches leaf/spine Nexus 9332D-GX2B y 9364D-GX2A. El diseño separa explícitamente los planos de tráfico para evitar que el tráfico de gestión o almacenamiento compita con el tráfico RDMA de entrenamiento. Forma parte de la familia de diseños AI POD de Cisco (Secure AI Factory con NVIDIA), con guías de despliegue específicas por proveedor de almacenamiento (NetApp, Pure Storage, VAST Data) publicadas por separado. Complementa al AI PODs (At a Glance) y al Data Center Networking Blueprint for AI/ML ya presentes en el catálogo con el diseño validado específico de entrenamiento/ fine-tuning.
