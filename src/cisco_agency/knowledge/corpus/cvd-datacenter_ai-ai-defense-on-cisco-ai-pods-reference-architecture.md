---
id: cvd-datacenter_ai-ai-defense-on-cisco-ai-pods-reference-architecture
title: AI Defense on Cisco AI PODs Reference Architecture
architecture: datacenter_ai
source: https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/UCS_CVDs/AI_defense_on_Cisco_AI_PODs_reference_architecture.html
source_date: '2026-09-15'
version: mar 2026
status: verificada
tags:
- ai
- architecture
- cisco
- cvd
- datacenter_ai
- defense
- 'on'
- pods
- reference
---
Arquitectura de referencia para desplegar Cisco AI Defense directamente sobre la infraestructura AI POD, manteniendo el procesamiento de Validación (detección) y Runtime (protección) dentro del entorno del propio cliente en lugar de depender solo de la nube de Cisco. La Validación ejecuta pruebas contra el modelo de IA alojado en el AI POD para generar guardrails específicos del modelo antes de producción. El Runtime se integra como gateway desplegado en línea, de forma que AI Defense puede inspeccionar en tiempo real el tráfico de entrada y salida del modelo o aplicación (prompt injection, fuga de datos sensibles, denegación de servicio, respuestas no deseadas). El diseño valida el despliegue sobre Red Hat OpenShift, con una opción de plano de control OpenShift basado en VMware, y define tres tamaños de referencia validados según carga esperada. Añade la capa de seguridad de IA (AI Defense) a los diseños AI POD de entrenamiento/fine-tuning ya incorporados al catálogo.
