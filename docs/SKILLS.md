# Skills

Una skill define **qué información necesita, qué decisión toma, cómo verifica sus
conclusiones y qué entrega**. Viven en `src/cisco_agency/skills/` (y las de diseño
están encapsuladas en los especialistas).

| Skill | Módulo | Entrada | Decisión | Entrega |
|-------|--------|---------|----------|---------|
| Descubrimiento del cliente | `customer_discovery` | dict YAML/JSON | Normaliza e infiere banderas de alcance | `Opportunity` |
| Diseño Secure Networking | `agents/secure_networking` | `Opportunity` | Acceso, identidad, segmentación, conectividad | `SpecialistFinding` |
| Diseño de ciberseguridad | `agents/security` | `Opportunity` | Zero Trust, micro-segmentación, NDR/EDR | `SpecialistFinding` |
| Diseño IT/OT | `agents/it_ot` | `Opportunity` | Zonas, sensores, comunicaciones | `SpecialistFinding` |
| Diseño de colaboración | `agents/collaboration` | `Opportunity` | UC, telefonía, salas, Contact Center | `SpecialistFinding` |
| Verificación de portafolio | `portfolio_verification` | `findings` | Evalúa sustento por evidencia | Resumen de cobertura y gaps |
| Integración entre arquitecturas | `integration` | `findings` | Flujos, políticas, responsabilidades | dict de integración |
| BOM y licenciamiento | `bom_licensing` | `findings` | Consolida sin duplicados | `Bom` |
| Caso financiero | `financial_case` | `Opportunity`, `Bom` | Escenarios y métricas | `FinancialCase` |
| Propuesta ejecutiva | `reporting/pdf_builder` | todo el estado | STAR, blueprint, roadmap | HTML + PDF |

## Formato común de entrega

```
Necesidad del cliente → solución propuesta → dependencias → dimensionamiento →
licencias → beneficio medible → evidencia → riesgos y pendientes
```

Implementado en `schemas.SpecialistFinding`. Permite al coordinador **comparar y
reconciliar** recomendaciones de forma homogénea.

## Evidencia

`schemas.Evidence` transporta `claim`, `source`, `source_date`, `version` y
`status` (`verificada` / `condicionada` / `pendiente`). El acceso a documentación
oficial, matrices de compatibilidad y precios se hace por **integración
autorizada** o documentos provistos por el equipo comercial — no se inventan.

## Añadir una skill

1. Crea `skills/mi_skill.py` con una función pura y tipada.
2. Expórtala en `skills/__init__.py`.
3. Conéctala como nodo en `graph.py` (o dentro de un nodo existente).
4. Añade una prueba en `tests/`.
