---
id: cvd-collaboration-cisco-preferred-architecture-for-webex-edge-connect
title: Cisco Preferred Architecture for Webex Edge Connect
architecture: collaboration
source: https://www.cisco.com/c/dam/en/us/td/docs/solutions/PA/EdgeConnect/PA_Edge_Connect_Design.pdf
source_date: '2026-09-28'
version: jul 2026
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
Arquitectura preferida para Webex Edge Connect, una conexión de peering de red privada y dedicada que conecta las instalaciones del cliente directamente con el backbone de Webex a través de un proveedor de cloud exchange (Equinix Fabric o Megaport), evitando el tránsito por Internet público. Requiere una conexión activa en el Equinix Cloud Exchange (o equivalente en Megaport) y un número de sistema autónomo (ASN) BGP público o privado para establecer el peering entre el router de borde del cliente y el backbone de Webex. El enlace es administrado, con calidad de servicio (QoS) habilitada y ancho de banda dedicado hacia el datacenter de Webex Meetings correspondiente, lo que aísla las reuniones y llamadas de la volatilidad y las amenazas asociadas al Internet público. Mejora la calidad y consistencia del rendimiento de reuniones y llamadas Webex, y aumenta la seguridad frente a conectividad basada en VPN o Internet directo. Complementa las arquitecturas de Webex Calling y Private Network Connect (PNC) ya cubiertas para clientes que requieren conectividad privada de máxima calidad hacia la nube de colaboración.
