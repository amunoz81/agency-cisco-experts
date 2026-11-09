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
Guía de diseño que detalla el AI POD de Cisco para entrenamiento y fine-tuning empresarial, combinando servidores UCS C885A M8 (fijo de 8 GPU, módulos NVIDIA SXM o AMD OAM) y UCS C845A M8 (PCIe, 2/4/6/8 GPUs) con dos fabrics independientes sobre switches Nexus 9000. El fabric backend (GPU-a-GPU) es spine-leaf de dos niveles sin bloqueo, con unidades de escala: Type 1 (dos leaf N9k-C9332D-GX2B) hasta 4 nodos C885A (32 GPUs), y Type 2 (dos leaf N9k-C9364D-GX2A) hasta 8 nodos (64 GPUs). En el C845A, dos GPUs comparten una NIC east-west, reduciendo el consumo de puertos de switch por nodo y elevando la densidad de GPU por unidad de escala frente al C885A. El fabric frontend maneja gestión, almacenamiento y tráfico de usuario; NVIDIA recomienda al menos 12.5 Gbps de ancho de banda de storage por GPU (100 Gbps para un C885A de 8 GPU). El diseño está avalado para la NVIDIA Enterprise Reference Architecture ERA 2-8-9-400, validado con C885A y Nexus 9000 contra los requisitos de ancho de banda y latencia de H200.
