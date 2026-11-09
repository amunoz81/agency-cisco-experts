---
id: cvd-collaboration-private-network-connect-for-webex-calling-multi-tenant-desig
title: Private Network Connect for Webex Calling Multi-Tenant Design Overview
architecture: collaboration
source: https://www.cisco.com/c/dam/en/us/td/docs/solutions/CVD/Collaboration/cloud/PA-PNC.pdf
source_date: '2026-09-15'
version: '2025'
status: verificada
tags:
- calling
- collaboration
- connect
- cvd
- design
- for
- multi
- network
- overview
- private
- tenant
- webex
---
Describe Private Network Connect (PNC), un enlace IP privado, administrado y con soporte de QoS entre la red del cliente y Webex Calling, que evita el tránsito del tráfico de voz por Internet público. Define dos modelos de interconexión: a nivel de partner, donde se agregan VPNs o redes IP privadas de múltiples clientes en una misma interconexión con una VLAN dedicada por cliente; y a nivel de cliente, donde todo el ancho de banda de la interconexión queda dedicado a una sola empresa. El aprovisionamiento de cada interconexión requiere un VLAN ID único, un ASN, direcciones IP en ambos extremos y una subred /29, /30 o /31; se recomienda configurar interconexiones y VLANs antes de migrar cualquier sitio a PNC. El alcance se limita a Webex Calling: el resto de cargas de Webex (Meetings, Messaging, Control Hub) sigue viajando por Internet (over the top). Al migrar un sitio deben actualizarse el Local Gateway y el proxy de salida de los teléfonos MPP, y resincronizar los equipos. Complementa el diseño de Webex Calling ya presente en el catálogo con la variante de conectividad privada.
