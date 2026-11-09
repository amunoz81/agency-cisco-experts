---
id: cvd-datacenter_ai-flexpod-with-cisco-ai-pod-infrastructure-for-ai-training-and
title: 'FlexPod with Cisco AI POD: Infrastructure for AI Training and Fine-Tuning
  Deployment Guide'
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/flexpod_aipod_training_manual.html
source_date: '2026-09-15'
version: feb 2026
status: verificada
tags:
- ai
- and
- cisco
- cvd
- datacenter_ai
- deployment
- fine
- flexpod
- for
- guide
- infrastructure
- pod
- training
- tuning
- with
---
Guía de despliegue que integra el AI POD de Cisco (servidores UCS C885A M8 con GPU) como tenant sobre una infraestructura FlexPod Datacenter ya desplegada (FlexPod Base), combinando cómputo Cisco con almacenamiento NetApp. El lado de storage usa controladores NetApp AFF A90 con FlexGroup, NFSv4.1 y RDMA, además de NVIDIA GPUDirect Storage para acceso directo de las GPU al almacenamiento sin pasar por la CPU, reduciendo la latencia en cargas de entrenamiento. Cubre configuración de switches, red GPU-a-GPU en el fabric backend, aprovisionamiento de storage ONTAP, acceso S3 para un tenant de OpenShift, grupos de recursos en Cisco Intersight y ejecución de NVIDIA Base Command Manager con corridas de ejemplo de MLPerf Training. También describe cómo añadir nodos C885A adicionales a un clúster OpenShift existente. Se apoya en el AI POD for Enterprise Training and Fine-Tuning Design Guide para el diseño de red y servidores, y complementa el blueprint de datacenter para IA/ML ya presente en el catálogo con una ruta de despliegue concreta sobre FlexPod.
