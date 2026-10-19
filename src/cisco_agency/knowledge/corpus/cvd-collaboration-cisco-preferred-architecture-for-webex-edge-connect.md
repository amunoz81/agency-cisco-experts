---
id: cvd-collaboration-cisco-preferred-architecture-for-webex-edge-connect
title: Cisco Preferred Architecture for Webex Edge Connect
architecture: collaboration
source: https://www.cisco.com/c/dam/en/us/td/docs/solutions/PA/EdgeConnect/PA_Edge_Connect_Design.pdf
source_date: '2026-09-15'
version: '2026'
status: verificada
tags:
- architecture
- cisco
- collaboration
- connect
- cvd
- edge
- for
- preferred
- webex
---
Webex Edge Connect es un enlace dedicado, con soporte de QoS, entre el sitio del cliente y la nube Webex, provisto a través de un proveedor de cloud exchange como Equinix o Megaport. El proveedor interconecta al cliente con un datacenter de Webex y enruta el tráfico destinado a Webex por un peering BGP directo: Cisco administra un extremo del peering de Capa 3 y el cliente el otro. Define arquitecturas para Meetings y Calling (incluida la variante Calling Multi-Tenant) y para Dedicated Instance, en este último caso con peering Edge Connect en dos sitios dentro de una región para redundancia. Requiere una conexión activa a Equinix (o equivalente), un ASN BGP propio y espacio de IP pública independiente del proveedor; no acepta anuncios de prefijos privados (RFC1918). Private Network Connect (PNC) es la variante para Webex Calling multi-tenant; otras cargas de Webex (Meetings, Mensajería, Control Hub) se acceden por Internet (OTT), no solo por PNC.
