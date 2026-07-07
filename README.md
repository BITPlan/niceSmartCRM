# niceSmartCRM
nicegui based Customer Relation Management tool

[![pypi](https://img.shields.io/pypi/pyversions/niceSmartCRM)](https://pypi.org/project/niceSmartCRM/)
[![Github Actions Build](https://github.com/BITPlan/niceSmartCRM/actions/workflows/build.yml/badge.svg)](https://github.com/BITPlan/niceSmartCRM/actions/workflows/build.yml)
[![PyPI Status](https://img.shields.io/pypi/v/niceSmartCRM.svg)](https://pypi.python.org/pypi/niceSmartCRM/)
[![GitHub issues](https://img.shields.io/github/issues/BITPlan/niceSmartCRM.svg)](https://github.com/BITPlan/niceSmartCRM/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/BITPlan/niceSmartCRM.svg)](https://github.com/BITPlan/niceSmartCRM/issues/?q=is%3Aissue+is%3Aclosed)
[![API Docs](https://img.shields.io/badge/API-Documentation-blue)](https://BITPlan.github.io/niceSmartCRM/)
[![License](https://img.shields.io/github/license/BITPlan/niceSmartCRM.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Migration 2026

niceSmartCRM replaces the legacy Java/Jersey/JPA smartCRM system. Both systems share the same
MariaDB `smartcrm` database during the transition; an anti-corruption layer
(`from_smartcrm()` classmethods in [crm/crm_core.py](crm/crm_core.py)) translates the German
database schema to the English Python domain model. The database schema is only migrated
to English naming once the Java system is decommissioned.

### Legacy model (German — Java/JPA/MariaDB)

![smartCRM legacy model](https://www.plantuml.com/plantuml/proxy?cache=no&fmt=svg&src=https://raw.githubusercontent.com/BITPlan/niceSmartCRM/main/docs/legacy_model.puml)

### Target model (English — Python dataclasses)

![niceSmartCRM domain model](https://www.plantuml.com/plantuml/proxy?cache=no&fmt=svg&src=https://raw.githubusercontent.com/BITPlan/niceSmartCRM/main/docs/english_model.puml)

PlantUML sources: [docs/legacy_model.puml](docs/legacy_model.puml) · [docs/english_model.puml](docs/english_model.puml)
