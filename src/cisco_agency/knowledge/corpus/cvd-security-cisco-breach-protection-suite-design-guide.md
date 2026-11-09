---
id: cvd-security-cisco-breach-protection-suite-design-guide
title: Cisco Breach Protection Suite Design Guide
architecture: security
source: https://www.cisco.com/c/en/us/solutions/collateral/enterprise/design-zone-security/breach-protection-suite-dg.html
source_date: '2026-09-15'
version: '2023'
status: verificada
tags:
- breach
- cisco
- cvd
- design
- guide
- protection
- security
- suite
---
Guía de diseño que integra los componentes del Cisco Breach Protection Suite bajo Cisco XDR como motor de correlación: Secure Endpoint (protección de endpoint), Email Threat Defense (protección del correo), Secure Client (acceso remoto), Secure Network Analytics (detección heurística de anomalías en tráfico de red mediante NetFlow) y Umbrella (seguridad DNS/SWG). XDR agrega la telemetría de estos productos para automatizar la investigación y reducir el tiempo de respuesta ante incidentes. Incluye pasos de integración por producto y pruebas de validación concretas (por ejemplo, detección de DNS rogue y bloqueo de DNS tunneling) para comprobar que la telemetría llega correctamente a XDR. El empaquetado por niveles (Essentials/Advantage) determina qué productos se incluyen; Secure Network Analytics suele formar parte del nivel superior. Sirve como referencia para dimensionar una arquitectura de detección y respuesta extendida apoyada en productos de seguridad Cisco existentes en lugar de una plataforma aislada, reforzando la integración end-to-end endpoint-red-correo-DNS.
