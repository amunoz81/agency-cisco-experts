# Guía de contribución

Gracias por colaborar en optimizar la Agencia de Expertos Cisco.

## Preparar el entorno

```bash
make install          # crea .venv e instala en modo editable con extras dev
cp .env.example .env   # opcional: para usar un LLM real
```

## Flujo de trabajo

1. Crea una rama desde `main`: `git checkout -b feat/mi-cambio`.
2. Trabaja en modo offline mientras desarrollas: `OFFLINE=true`.
3. Antes de abrir PR:
   ```bash
   make fmt    # formatea
   make lint   # ruff + mypy
   make test   # pruebas
   make demo   # verifica que la propuesta se genera
   ```
4. Abre un Pull Request describiendo el cambio y su impacto.

## Convenciones

- Código y prompts en **español** (audiencia del proyecto).
- Todo hallazgo de especialista debe respetar el **formato común**
  (`SpecialistFinding`) y declarar **evidencia** con estado.
- Los cálculos financieros van en `finance/` con **fórmulas reproducibles** y
  pruebas; nada de números mágicos sin supuesto declarado.
- No incorpores **precios reales ni SKUs definitivos** en el código: son datos por
  oportunidad. Usa placeholders claramente marcados.
- No subas `.env` ni credenciales.

## Estructura de un cambio típico

- ¿Nuevo especialista? → `docs/AGENTS.md` §"Añadir un especialista nuevo".
- ¿Nueva skill? → `docs/SKILLS.md` §"Añadir una skill".
- ¿Nuevo formato de salida? → `reporting/` (plantilla Jinja2 + `pdf_builder.py`).

## Estilo

- `ruff` con line-length 100 (ver `pyproject.toml`).
- Prefiere funciones puras y tipadas; el estado del grafo es explícito.
