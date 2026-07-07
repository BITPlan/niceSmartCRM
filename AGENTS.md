# AGENTS.md - niceSmartCRM

## Project Overview

niceSmartCRM is a Python/NiceGUI replacement for the legacy Java-based smartCRMRest system.
The goal is to incrementally migrate all CRM functionality from Java (Jersey/JPA/JAXB) to
Python while sharing the same MariaDB `smartcrm` database during the transition period.

- **GitHub**: https://github.com/BITPlan/niceSmartCRM
- **Wiki**: https://wiki.bitplan.com/index.php/niceSmartCRM
- **Media Wiki**: https://media.bitplan.com/index.php/NiceSmartCRM
- **Legacy whitebox docs**: https://media.bitplan.com/index.php/SmartCRM/REST/Whitebox
- **Legacy REST API docs**: https://media.bitplan.com/index.php/SmartCRM/REST
- **Migration plan**: https://media.bitplan.com/index.php/SmartCRM/Migration2026
- **Agent**: [Agent/Guido](https://media.bitplan.com/index.php/Agent/Guido) — Python developer agent following BITPlan conventions
- **Agent rules**: [Agent/Guido/BITPlan](https://media.bitplan.com/index.php/Agent/Guido/BITPlan) — canonical BITPlan Python conventions

## Open Issues

- **#3** [migrate from smartCRM SQL](https://github.com/BITPlan/niceSmartCRM/issues/3) — core migration task (milestone 0.0.1)
- **#4** [Look for Formset/Form/Group/Field description format](https://github.com/BITPlan/niceSmartCRM/issues/4) — UI form description research

## Architecture

### Anti-Corruption Layer Strategy

The project uses an **anti-corruption layer** to isolate the new Python domain model from
the legacy German-named MariaDB schema. The key principle:

> **Do NOT modify the database schema.** The legacy Java system and the new Python system
> share the same MariaDB database. The DB schema will only be migrated to English naming
> after the Python solution is proven reliable and the Java system is decommissioned.

Data flow:

```
MariaDB (German schema)
        |
  SmartCRMAdapter (crm/smartcrm_adapter.py)
        |
  from_smartcrm() classmethods (German -> English field mapping)
        |
  Python @dataclass domain models (English names)
        |
  +-----+----------+
  |                 |
MogwaiGraph     FastAPI REST
(NiceGUI UI)    (crm/crm_rest.py, read-only)
```

When the database is unreachable, both the web server and the REST API fall
back to the JSON exports in `~/.smartcrm/`; DB-dependent tests skip gracefully.

### Entity Mapping

The legacy Java system manages 8 entities. All are covered read-only since 2026-07-07.

| English Name   | Legacy DB Table  | Legacy REST Path   | Python Status | Python Class   |
|----------------|------------------|--------------------|---------------|----------------|
| Organization   | `organisation`   | `/organisation(s)` | Implemented   | `Organization` |
| Person         | `person`         | `/person(s)`       | Implemented   | `Person`       |
| Contact        | `kontakt`        | `/kontakt(s)`      | Implemented   | `Contact`      |
| Invoice        | `rechnung`       | `/rechnung(s)`     | Implemented   | `Invoice`      |
| Email          | `email`          | `/email(s)`        | Implemented   | `Email`        |
| Project        | `projekt`        | `/projekt(s)`      | Implemented   | `Project`      |
| Action         | `aktion`         | `/aktion(s)`       | Implemented   | `Action`       |
| Todo           | `todo`           | `/todo(s)`         | Implemented   | `Todo`         |

### Key Relationships (from legacy JPA model)

- **Person** belongs to an **Organization** (via `meineOrganisation_OrganisationNummer`)
- **Contact** belongs to a **Person** (via `meinePerson_PersonNummer`)
- **Contact** may reference an **Action** (via `wgAktion_AktionNummer`)
- **Invoice** references an **Organization** (via `Auftraggeber_OrganisationNummer`)
- **Invoice** may reference a **Project** (via `ZuordnungProjekt_ProjektNummer`)

## Key Files

| File | Purpose |
|------|---------|
| `crm/crm_core.py` | Domain model `@dataclass` definitions with `from_smartcrm()` field mapping |
| `crm/smartcrm_adapter.py` | `SmartCRMAdapter` — reads from DB/JSON, maps legacy topic names to Python classes |
| `crm/db.py` | Raw PyMySQL database wrapper (read-only, `DictCursor`) |
| `crm/crm_web.py` | NiceGUI web server — loads data into `MogwaiGraph`, serves UI views, mounts REST API |
| `crm/crm_rest.py` | `CrmRestApi` — read-only FastAPI `APIRouter` (`/api/{plural}`, `/api/{plural}/{id}`) |
| `crm/crm_cmd.py` | CLI entry point (`smartcrm` command) |
| `crm/xmi.py` | UML/XMI model parser for the legacy SmartCRM model |
| `crm/resources/crm-schema.yaml` | Graph schema for mogwai (node type configs, icons, display order) |
| `crm/resources/queries.yaml` | Named SQL/Ask query templates |
| `crm/resources/i18n/en.yaml` | English translations |
| `crm/resources/i18n/de.yaml` | German translations |
| `tests/test_crm_core.py` | Tests for domain models and SmartCRMAdapter |
| `tests/test_crm_rest.py` | Tests for the REST API (FastAPI TestClient, JSON data source) |
| `tests/test_db.py` | Tests for direct MySQL queries |

## Coding Conventions

This project follows the [Agent/Guido/BITPlan](https://media.bitplan.com/index.php/Agent/Guido/BITPlan)
conventions. Key points summarized below; the wiki page is the canonical source.

### Style

- **Formatter**: `black` + `isort` — always run `scripts/blackisort` before committing.
- **Line length**: 88 characters (black default).
- **Docstrings**: Google-style with type hints on all public functions and classes.
- **Return style**: Always use a named return variable. No direct expression returns.
- **Imports**: Top-level only, absolute imports preferred. Three groups separated by blank lines:
  stdlib, third-party, local.
- **Type annotations**: Required on all function signatures. Use `Optional[X]` (not `X | None`).
- **No `from __future__ import annotations`**.
- **No ruff/flake8/pylint/mypy** unless explicitly configured.

### Naming

- **Classes**: PascalCase (`Organization`, `SmartCRMAdapter`)
- **Functions/methods (new)**: snake_case (`from_smartcrm`, `execute_query`)
- **Functions/methods (legacy)**: camelCase kept for compatibility
- **Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Test files**: `tests/test_<module>.py`
- **Test classes**: `TestXxx` (PascalCase)
- **All new code uses English names** for classes, fields, variables, and API paths.
- The `from_smartcrm(data: Dict)` classmethod on each dataclass is the **single point**
  where German-to-English field translation happens. Never leak German names beyond this method.
- Example: DB column `Branche` -> Python field `industry`, DB column `Vorname` -> `first_name`.

### Testing

- **Framework**: `unittest` (not pytest). All test classes inherit from `Basetest`
  (from `ngwidgets.basetest` or `basemkit.basetest`).
- **No pytest fixtures or conftest.py.**
- **`Basetest.inPublicCI()`** for skipping tests that need local resources (e.g., DB).
- **`scripts/test` must be green** before committing.

### Quality Assurance

Run `checkos` to verify project compliance:

```bash
checkos -o BITPlan -p niceSmartCRM --local -v -ws /Users/wf/py-workspace
```

### Adding a New Entity

To add one of the missing entities (Email, Project, Action, Todo):

1. **Define the dataclass** in `crm/crm_core.py`:
   - Use English field names with `Optional` typing where appropriate.
   - Add a `from_smartcrm(cls, data: Dict)` classmethod mapping German DB columns to English fields.
   - Reference the legacy field names from [SmartCRM/REST](https://media.bitplan.com/index.php/SmartCRM/REST).

2. **Register the topic** in `SmartCRMAdapter.get_topics()` in `crm/smartcrm_adapter.py`:
   - Add a `smartCRMTopic(name=..., plural_name=..., dataclass=..., table_name=..., node_path=...)`.
   - `table_name` is the German MySQL table name (e.g., `projekt`).
   - `node_path` follows the pattern `{Manager}/{plural}/{Entity}` (e.g., `ProjektManager/projekts/Projekt`).

3. **Add to graph schema** in `crm/resources/crm-schema.yaml`:
   - Define icon, key_field, display_order, and label.

4. **Add i18n keys** in `crm/resources/i18n/en.yaml` and `de.yaml`.

5. **Write tests** in `tests/test_crm_core.py`.

### REST API (read-only since 2026-07-07 — FastAPI)

NiceGUI runs on FastAPI, so the REST API is a FastAPI `APIRouter`
(`crm/crm_rest.py`) mounted into the same application:

- **Read endpoints** (done): `GET /api/{plural}` (with `limit`/`offset`) and
  `GET /api/{plural}/{id}` for all 8 entities, English naming
  (e.g., `/api/organizations`, `/api/persons`, `/api/todos`).
- **OpenAPI docs**: auto-generated at `/docs`.
- **Write endpoints**: POST/PUT/DELETE once read operations are stable.
- **Same database**: FastAPI reads/writes to the same MariaDB `smartcrm` DB via the
  anti-corruption layer, with JSON-export fallback when the DB is unreachable.
- **Open**: search / find-by-attribute endpoints mirroring the legacy
  `/{entities}/by/{attr}/{value}` and `/{entities}/search`.

## Database Configuration

Connection config is read from `~/.smartcrm/db_config.yaml`:

```yaml
database:
  host: <hostname>
  user: <username>
  password: <password>
  name: smartcrm
```

The database is MariaDB 10.11, running in Docker alongside the legacy Java REST server.
Both the Java and Python systems connect to the same database instance.

## Running

```bash
# Install
pip install .

# Run the NiceGUI web server (default port 9854)
smartcrm

# Format code before committing
scripts/blackisort

# Run tests (must pass before committing)
scripts/test

# Check project compliance
checkos -o BITPlan -p niceSmartCRM --local -v
```

## Migration Phases

See [SmartCRM/Migration2026](https://media.bitplan.com/index.php/SmartCRM/Migration2026) for the full plan.

1. **Entity coverage** — done 2026-07-07: Email, Project, Action, Todo dataclasses and adapters.
2. **FastAPI REST API** — read endpoints done 2026-07-07; search/find-by-attribute still open.
3. **Write operations** — Currently read-only; add create/update/delete.
   Precondition: DB access from the dev environment (grants only cover `%.bitplan.com`
   hosts) — or a local MariaDB provisioned from the daily backup dump on host `r`.
4. **DB schema migration** — Rename tables and columns to English. **Only after Java is switched off.**

## History

- **2007**: SmartCRM MySQL migration (from Lotus Notes/Delphi)
- **2018**: Java/JPA code generated with smartGENERATOR
- **2024-01**: niceSmartCRM Python project started ([SmartCRM 2024](https://media.bitplan.com/index.php/SmartCRM_2024) workpackage)
- **2026**: Migration 2026 — complete the transition, add FastAPI REST, decommission Java
