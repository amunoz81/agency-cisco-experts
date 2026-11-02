---
id: cvd-security-secure-remote-worker-for-on-prem-design-guide
title: Secure Remote Worker for On-Prem Design Guide
architecture: security
source: https://www.cisco.com/c/en/us/solutions/collateral/enterprise/design-zone-security/srw-on-prem.html
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- cvd
- design
- for
- guide
- 'on'
- prem
- remote
- secure
- security
- worker
---
Guía de diseño para trabajadores remotos que acceden a aplicaciones on-premises mediante VPN. Combina Cisco Secure Client (VPN de acceso remoto) terminada en Secure Firewall (Firepower Threat Defense sobre appliance Firepower 4100) con Duo para MFA y verificación de postura del dispositivo, Umbrella para protección DNS/web del usuario remoto y Secure Endpoint para protección de malware en el endpoint. Incluye pasos de configuración en Firewall Management Center (FMC) para el perfil de conexión VPN, grupos de túnel y políticas de grupo. El diseño prioriza acceso cifrado punto a punto hasta el firewall perimetral, aplicación de MFA antes de establecer el túnel y verificación continua de postura (parcheo, antivirus, cifrado de disco) antes de autorizar el acceso. Sirve como arquitectura base de VPN de acceso remoto dentro del marco Zero Trust de Cisco, complementaria a las guías Zero Trust Network/Cloud y Zero Trust User/Device, que asumen el concentrador VPN ya configurado según esta guía.
