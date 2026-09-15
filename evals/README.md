# Evaluaciones (evals)

Batería de pruebas de comportamiento del pipeline sobre un **dataset dorado** de
oportunidades. Se ejecutan en modo offline (determinista), sin costo de tokens.

```bash
make eval                       # o: cisco-agency eval
```

## Estructura de un caso (`cases/*.yaml`)

```yaml
name: mi_caso
opportunity:            # misma forma que una ficha de oportunidad
  customer: "..."
  sites: [...]
  it_ot_present: true
expect:
  specialists_include: [secure_networking, security]   # deben aparecer
  specialists_exclude: [it_ot]                          # no deben aparecer
  min_findings: 2
  min_bom_lines: 10
  no_duplicate_bom: true
  review_passes: true
  min_verified_evidence: 2
  proposal_generated: true
```

## Qué verifican

- **Alcance correcto**: los especialistas convocados coinciden con lo esperado.
- **BOM**: mínimo de líneas y ausencia de duplicados.
- **Evidencia**: mínimo de evidencia verificada (grounding).
- **Revisión**: la revisión técnica aprueba (sin bloqueantes).
- **Entrega**: se genera la propuesta.

Añade casos nuevos creando un `.yaml` en `cases/`. La CI corre `cisco-agency eval`
y las pruebas incluyen `tests/test_evals.py`, así que un caso fallido rompe el build.
