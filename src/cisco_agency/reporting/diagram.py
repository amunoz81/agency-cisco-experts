"""Diagrama de arquitectura de red.

Construye una topología por niveles (tiers) a partir de las arquitecturas que el
cliente necesita y la renderiza como:
- PNG (Pillow) con dispositivos estilo Cisco y badges de nube (AWS/Azure/GCP),
  para incrustar en la propuesta HTML/PDF/PPTX/DOCX.
- .drawio (diagrams.net) editable, importable a Lucidchart, con estilos de las
  bibliotecas oficiales Cisco/AWS/Azure/GCP.

Los glifos del PNG son originales (paleta Cisco), no stencils con copyright.
"""

from __future__ import annotations

import html
from pathlib import Path

from ..schemas import Opportunity, SpecialistFinding

# Colores por dominio (RGB)
NET = (0x1B, 0xA0, 0xD7)
SEC = (0x1A, 0xB2, 0x4B)
DC = (0x6F, 0x42, 0xC1)
OT = (0xE8, 0x83, 0x3A)
SOC = (0x2F, 0x6F, 0xB0)
COLLAB = (0x14, 0xB8, 0xA6)
CLOUD = (0x5B, 0x6B, 0x7A)
NAVY = (0x0D, 0x27, 0x4D)
INK = (0x1A, 0x1A, 0x1A)
LINE = (0xC7, 0xD6, 0xE5)

PROVIDER_COLOR = {
    "aws": (0xFF, 0x99, 0x00),
    "amazon": (0xFF, 0x99, 0x00),
    "azure": (0x00, 0x78, 0xD4),
    "microsoft": (0x00, 0x78, 0xD4),
    "google": (0x42, 0x85, 0xF4),
    "gcp": (0x42, 0x85, 0xF4),
    "oracle": (0xC7, 0x46, 0x34),
    "ibm": (0x1F, 0x70, 0xC1),
}

# kind -> estilo de shape en draw.io (bibliotecas oficiales; si el nombre no
# resuelve, draw.io/Lucidchart muestran la caja con la etiqueta).
DRAWIO_SHAPE = {
    "cloud": "shape=cloud;",
    "sase": "shape=cloud;",
    "firewall": "shape=mxgraph.cisco.security.firewall;",
    "switch": "shape=mxgraph.cisco.switches.workgroup_switch;",
    "router": "shape=mxgraph.cisco.routers.router;",
    "wifi": "shape=mxgraph.cisco.wireless.wireless_access_point;",
    "server": "shape=mxgraph.cisco.servers.standard_host;",
    "identity": "shape=mxgraph.cisco.servers.directory_server;",
    "sensor": "shape=mxgraph.cisco.misc.generic_building;",
    "shield": "shape=mxgraph.cisco.security.secure_server;",
    "chart": "shape=mxgraph.cisco.storage.dual_mode_ap;",
    "phone": "shape=mxgraph.cisco.modules.ip_phone;",
}


class Node:
    def __init__(self, label, kind="box", color=NET):
        self.label = label
        self.kind = kind
        self.color = color
        self.x = self.y = self.w = self.h = 0


class Tier:
    def __init__(self, label, color):
        self.label = label
        self.color = color
        self.nodes: list[Node] = []


def build_topology(opportunity: Opportunity, findings: list[SpecialistFinding]) -> list[Tier]:
    present = {f.architecture.value for f in findings}
    tiers: list[Tier] = []

    # 1. Nube y acceso seguro
    t = Tier("Nube y acceso seguro", CLOUD)
    t.nodes.append(Node("Internet", "cloud", CLOUD))
    for p in opportunity.cloud_providers:
        color = next((v for k, v in PROVIDER_COLOR.items() if k in p.lower()), CLOUD)
        t.nodes.append(Node(p, "cloud", color))
    if present & {"secure_networking", "security"}:
        t.nodes.append(Node("Cisco Secure Access (SSE)", "sase", SEC))
    tiers.append(t)

    # 2. Perímetro y WAN
    t = Tier("Perímetro y WAN", SEC)
    if "security" in present:
        t.nodes.append(Node("Secure Firewall", "firewall", SEC))
    if "secure_networking" in present:
        t.nodes.append(Node("SD-WAN / Catalyst Edge", "router", NET))
    if t.nodes:
        tiers.append(t)

    # 3. Campus e identidad
    if "secure_networking" in present:
        t = Tier("Campus e identidad", NET)
        t.nodes.append(Node("Catalyst Core", "switch", NET))
        t.nodes.append(Node("Cisco ISE", "identity", NET))
        t.nodes.append(Node("Cisco DUO (MFA)", "shield", SEC))
        t.nodes.append(Node("Wireless (Meraki/9800)", "wifi", NET))
        tiers.append(t)

    # 4. Data Center
    if "datacenter_ai" in present:
        t = Tier("Data Center y AI", DC)
        t.nodes.append(Node("Nexus Fabric", "switch", DC))
        t.nodes.append(Node("UCS / AI POD", "server", DC))
        if "security" in present:
            t.nodes.append(Node("Secure Workload / Hypershield", "shield", SEC))
        tiers.append(t)

    # 5. IT/OT industrial
    if "it_ot" in present:
        t = Tier("IT/OT industrial", OT)
        t.nodes.append(Node("IDMZ Firewall", "firewall", SEC))
        t.nodes.append(Node("Catalyst IE + sensor", "switch", OT))
        t.nodes.append(Node("Cyber Vision", "sensor", OT))
        tiers.append(t)

    # 6. Observabilidad / SOC
    if "observability_soc" in present:
        t = Tier("Observabilidad / SOC", SOC)
        t.nodes.append(Node("Splunk (SIEM/SOAR)", "chart", SOC))
        t.nodes.append(Node("ThousandEyes", "chart", SOC))
        tiers.append(t)

    # 7. Colaboración
    if "collaboration" in present:
        t = Tier("Colaboración (Webex)", COLLAB)
        t.nodes.append(Node("Webex Suite / Calling", "phone", COLLAB))
        t.nodes.append(Node("Control Hub", "server", COLLAB))
        tiers.append(t)

    return tiers


# --------------------------------------------------------------------------
# Layout (asigna x/y/w/h a cada nodo) — compartido por PNG y drawio
# --------------------------------------------------------------------------
W = 1320
LABEL_X, LABEL_W = 24, 190
AREA_X0, AREA_X1 = 232, W - 24
TITLE_H = 56
TIER_H = 138
NODE_H = 92
NODE_GAP = 20


def layout(tiers: list[Tier]) -> int:
    y = TITLE_H + 16
    for t in tiers:
        n = len(t.nodes)
        area = AREA_X1 - AREA_X0
        nw = min(230, (area - (n - 1) * NODE_GAP) / max(n, 1))
        total = n * nw + (n - 1) * NODE_GAP
        x = AREA_X0 + (area - total) / 2
        for node in t.nodes:
            node.x, node.y, node.w, node.h = int(x), int(y + (TIER_H - NODE_H) / 2), int(nw), NODE_H
            x += nw + NODE_GAP
        y += TIER_H
    return int(y + 24)


# --------------------------------------------------------------------------
# PNG (Pillow)
# --------------------------------------------------------------------------
def _font(size):
    from PIL import ImageFont

    return ImageFont.load_default(size=size)


def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:3]


def _glyph(d, kind, cx, cy, s, color):
    """Dibuja un glifo de dispositivo (original, paleta Cisco)."""
    r = s // 2
    x0, y0, x1, y1 = cx - r, cy - r, cx + r, cy + r
    if kind in ("cloud", "sase"):
        d.ellipse([x0, cy - r // 2, cx, y1], fill=color)
        d.ellipse([cx - r // 2, y0, cx + r // 2, y1], fill=color)
        d.ellipse([cx, cy - r // 2, x1, y1], fill=color)
        d.rectangle([x0 + 2, cy, x1 - 2, y1], fill=color)
    elif kind == "firewall":
        d.rectangle([x0, y0, x1, y1], fill=color)
        for i in range(1, 3):
            d.line([x0, y0 + i * s // 3, x1, y0 + i * s // 3], fill=(255, 255, 255), width=2)
        d.line([cx, y0, cx, y0 + s // 3], fill=(255, 255, 255), width=2)
        d.line([x0 + s // 3, y0 + s // 3, x0 + s // 3, y0 + 2 * s // 3],
               fill=(255, 255, 255), width=2)
    elif kind == "switch":
        d.rounded_rectangle([x0, cy - r // 2, x1, cy + r // 2], radius=3, fill=color)
        for i in range(4):
            px = x0 + 4 + i * (s - 8) // 4
            d.rectangle([px, cy + 1, px + 3, cy + r // 2 - 2], fill=(255, 255, 255))
    elif kind == "router":
        d.ellipse([x0, y0, x1, y1], fill=color)
        d.line([cx - r // 2, cy, cx + r // 2, cy], fill=(255, 255, 255), width=2)
        d.polygon([(cx + r // 2, cy - 3), (cx + r // 2 + 3, cy), (cx + r // 2, cy + 3)],
                  fill=(255, 255, 255))
    elif kind == "wifi":
        for rr in (r, int(r * 0.66), int(r * 0.33)):
            d.arc([cx - rr, cy - rr + r // 2, cx + rr, cy + rr + r // 2],
                  200, 340, fill=color, width=3)
        d.ellipse([cx - 3, cy + r // 2 - 3, cx + 3, cy + r // 2 + 3], fill=color)
    elif kind in ("server", "identity"):
        d.rounded_rectangle([cx - r // 2, y0, cx + r // 2, y1], radius=3, fill=color)
        for i in range(3):
            d.line([cx - r // 2 + 3, y0 + 5 + i * 6, cx + r // 2 - 3, y0 + 5 + i * 6],
                   fill=(255, 255, 255), width=2)
    elif kind == "shield":
        d.polygon([(cx, y0), (x1, y0 + 4), (x1, cy), (cx, y1), (x0, cy), (x0, y0 + 4)], fill=color)
        d.line([cx - 4, cy, cx - 1, cy + 4], fill=(255, 255, 255), width=2)
        d.line([cx - 1, cy + 4, cx + 5, cy - 4], fill=(255, 255, 255), width=2)
    elif kind == "sensor":
        d.regular_polygon((cx, cy, r), n_sides=6, fill=color)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255))
    elif kind == "chart":
        d.rounded_rectangle([x0, y0, x1, y1], radius=3, fill=color)
        for i, hh in enumerate((s // 3, s // 2, int(s * 0.7))):
            bx = x0 + 5 + i * 8
            d.rectangle([bx, y1 - 4 - hh, bx + 5, y1 - 4], fill=(255, 255, 255))
    elif kind == "phone":
        d.rounded_rectangle([cx - r // 2, y0, cx + r // 2, y1], radius=4, fill=color)
        d.rectangle([cx - r // 3, y0 + 5, cx + r // 3, cy + 2], fill=(255, 255, 255))
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=color)


def render_png(tiers: list[Tier], out_dir: str | Path, basename: str, customer: str) -> str:
    from PIL import Image, ImageDraw

    height = layout(tiers)
    img = Image.new("RGB", (W, height), (0xF7, 0xFA, 0xFD))
    d = ImageDraw.Draw(img)
    f_title, f_tier, f_node = _font(22), _font(13), _font(12)

    d.text((24, 16), f"Diagrama de arquitectura de red - {customer}",
           font=f_title, fill=NAVY)
    d.line([24, TITLE_H, W - 24, TITLE_H], fill=(0x00, 0xBC, 0xEB), width=3)

    # Espina vertical central conectando los tiers
    if tiers:
        spine = (AREA_X0 + AREA_X1) // 2
        y_first = tiers[0].nodes[0].y + NODE_H // 2
        y_last = tiers[-1].nodes[0].y + NODE_H // 2
        d.line([spine, y_first, spine, y_last], fill=LINE, width=3)

    for t in tiers:
        ty = t.nodes[0].y
        # Etiqueta del tier (izquierda)
        d.rounded_rectangle([LABEL_X, ty + 10, LABEL_X + LABEL_W, ty + NODE_H - 10],
                            radius=8, fill=t.color)
        for i, line in enumerate(_wrap(d, t.label, f_tier, LABEL_W - 16)):
            d.text((LABEL_X + 12, ty + 20 + i * 16), line, font=f_tier, fill=(255, 255, 255))
        # Nodos
        for node in t.nodes:
            d.rounded_rectangle([node.x, node.y, node.x + node.w, node.y + node.h],
                                radius=10, fill=(255, 255, 255), outline=node.color, width=2)
            d.rounded_rectangle([node.x, node.y, node.x + node.w, node.y + 7],
                                radius=3, fill=node.color)
            _glyph(d, node.kind, node.x + 26, node.y + 44, 30, node.color)
            tx = node.x + 48
            lines = _wrap(d, node.label, f_node, node.w - 56)
            oy = node.y + 30 + (max(0, 3 - len(lines))) * 8
            for i, line in enumerate(lines):
                d.text((tx, oy + i * 15), line, font=f_node, fill=INK)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"diagrama_{basename}.png"
    img.save(path)
    return str(path)


# --------------------------------------------------------------------------
# draw.io (diagrams.net) — editable, importable a Lucidchart
# --------------------------------------------------------------------------
def to_drawio(tiers: list[Tier], customer: str) -> str:
    layout(tiers)
    cells = []
    cid = 2
    tier_first = []
    for t in tiers:
        for j, node in enumerate(t.nodes):
            shape = DRAWIO_SHAPE.get(node.kind, "rounded=1;")
            hexc = "#{:02X}{:02X}{:02X}".format(*node.color)
            style = (f"{shape}html=1;whiteSpace=wrap;fillColor={hexc};strokeColor={hexc};"
                     "fontColor=#0d274d;fontSize=11;verticalLabelPosition=bottom;"
                     "verticalAlign=top;")
            label = html.escape(node.label)
            cells.append(
                f'<mxCell id="n{cid}" value="{label}" style="{style}" vertex="1" parent="1">'
                f'<mxGeometry x="{node.x}" y="{node.y}" width="{node.w}" height="{node.h}" '
                f'as="geometry"/></mxCell>'
            )
            node._id = f"n{cid}"  # type: ignore[attr-defined]
            if j == 0:
                tier_first.append(node)
            cid += 1
    # Aristas entre tiers (flujo vertical)
    for a, b in zip(tier_first, tier_first[1:], strict=False):
        cells.append(
            f'<mxCell id="e{cid}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;'
            f'strokeColor=#5b6b7a;" edge="1" parent="1" source="{a._id}" target="{b._id}">'  # type: ignore[attr-defined]
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        cid += 1
    title = html.escape(f"Arquitectura de red - {customer}")
    body = "".join(cells)
    return (
        '<mxfile host="cisco-experts-agency">'
        f'<diagram name="{title}">'
        '<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" '
        'connect="1" arrows="1" page="1" pageWidth="1320" pageHeight="900" math="0" shadow="0">'
        '<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        f'{body}</root></mxGraphModel></diagram></mxfile>'
    )


def write_drawio(tiers: list[Tier], out_dir: str | Path, basename: str, customer: str) -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"diagrama_{basename}.drawio"
    path.write_text(to_drawio(tiers, customer), encoding="utf-8")
    return str(path)
