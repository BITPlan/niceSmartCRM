"""
Created on 2026-09-23

@author: wf

field descriptors of the niceSmartCRM entities read from fields.yaml:
the single source for the German column to English field mapping,
the en/de labels, the English SQL views and the dataclass conversion
see https://github.com/BITPlan/niceSmartCRM/issues/6
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class FieldSpec:
    """
    one field of an entity: English name, legacy column and labels
    """

    name: str
    en: str
    de: str
    column: Optional[str] = None
    json: Optional[str] = None  # spelling of the JAXB export where it differs
    type: str = "str"  # str, int, float, bool, datetime
    pk: bool = False
    reference: Optional[str] = None  # referenced entity
    default: Any = None

    def label(self, lang: str = "en") -> str:
        """
        get the label in the given language

        Args:
            lang (str): en or de

        Returns:
            str: the label
        """
        label = self.de if lang == "de" else self.en
        return label

    def raw_value(self, record: Dict) -> Any:
        """
        get the raw value of this field from a legacy record

        Args:
            record (Dict): a row of the legacy table or an element of the JAXB export

        Returns:
            Any: the raw value, the column spelling first, the json spelling second
        """
        raw = record.get(self.column) if self.column else None
        if raw is None and self.json:
            raw = record.get(self.json)
        if raw is None:
            raw = self.default
        return raw

    def convert(self, record: Dict) -> Any:
        """
        get the converted value of this field from a legacy record

        Args:
            record (Dict): a row of the legacy table or an element of the JAXB export

        Returns:
            Any: the value converted per type
        """
        # local import: crm_core imports this module for its from_smartcrm methods
        from crm.crm_core import TypeConverter

        converters = {
            "datetime": TypeConverter.to_datetime,
            "int": TypeConverter.to_int,
            "bool": TypeConverter.to_bool,
            "float": TypeConverter.to_float,
        }
        raw = self.raw_value(record)
        converter = converters.get(self.type)
        value = converter(raw) if converter else raw
        return value


@dataclass
class EntitySpec:
    """
    one entity: its table, labels and fields
    """

    name: str
    en: str
    de: str
    table: Optional[str] = None
    plural: Optional[str] = None
    plural_en: Optional[str] = None
    plural_de: Optional[str] = None
    icon: Optional[str] = None
    fields: Dict[str, FieldSpec] = field(default_factory=dict)

    @property
    def pk(self) -> Optional[FieldSpec]:
        """
        the primary key field
        """
        pk = None
        for field_spec in self.fields.values():
            if field_spec.pk:
                pk = field_spec
                break
        return pk

    def plural_label(self, lang: str = "en") -> str:
        """
        get the plural label in the given language
        """
        label = self.plural_de if lang == "de" else self.plural_en
        return label

    def convert(self, record: Dict) -> Dict[str, Any]:
        """
        convert a legacy record to a dict of English field names and converted values

        Args:
            record (Dict): a row of the legacy table or an element of the JAXB export

        Returns:
            Dict[str, Any]: field name to value
        """
        values = {
            name: field_spec.convert(record) for name, field_spec in self.fields.items()
        }
        return values

    def view_name(self) -> str:
        """
        the name of the English view: the table name of the entity in English
        """
        view_name = self.name.lower()
        return view_name

    def view_ddl(self, view_db: str, source_db: str) -> str:
        """
        the DDL of the English view over the legacy table

        Args:
            view_db (str): the database holding the views
            source_db (str): the database holding the legacy tables

        Returns:
            str: the CREATE OR REPLACE VIEW statement
        """
        selects = []
        for field_spec in self.fields.values():
            if field_spec.column:
                selects.append(f"  `{field_spec.column}` AS `{field_spec.name}`")
        select_clause = ",\n".join(selects)
        ddl = (
            f"CREATE OR REPLACE VIEW `{view_db}`.`{self.view_name()}` AS\n"
            f"SELECT\n{select_clause}\n"
            f"FROM `{source_db}`.`{self.table}`;"
        )
        return ddl


class Fields:
    """
    the field descriptors of all entities as read from fields.yaml
    """

    _instance: Optional["Fields"] = None

    def __init__(self, yaml_path: Optional[str] = None):
        """
        constructor

        Args:
            yaml_path (str): the fields.yaml to read, the resource of the module by default
        """
        if yaml_path is None:
            yaml_path = Fields.default_path()
        self.yaml_path = yaml_path
        self.entities: Dict[str, EntitySpec] = {}
        self.load()

    @classmethod
    def default_path(cls) -> str:
        """
        the fields.yaml of the module resources
        """
        module_path = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(module_path, "resources", "fields.yaml")
        return yaml_path

    @classmethod
    def get(cls) -> "Fields":
        """
        the shared instance
        """
        if cls._instance is None:
            cls._instance = Fields()
        return cls._instance

    def load(self):
        """
        read the yaml
        """
        with open(self.yaml_path, "r") as yaml_file:
            data = yaml.safe_load(yaml_file)
        for entity_name, entity_data in data["fields"].items():
            meta = dict(entity_data.get("_", {}))
            entity = EntitySpec(name=entity_name, **meta)
            for field_name, field_data in entity_data.items():
                if field_name == "_":
                    continue
                entity.fields[field_name] = FieldSpec(name=field_name, **field_data)
            self.entities[entity_name] = entity

    def entity(self, name: str) -> EntitySpec:
        """
        get the entity spec of the given name
        """
        entity = self.entities[name]
        return entity

    def tables(self) -> List[EntitySpec]:
        """
        the entities backed by a legacy table
        """
        tables = [entity for entity in self.entities.values() if entity.table]
        return tables

    def to_dataclass(self, dataclass_type: type, record: Dict) -> Any:
        """
        convert a legacy record to an instance of the given dataclass

        Args:
            dataclass_type (type): the dataclass, its name is the entity name
            record (Dict): a row of the legacy table or an element of the JAXB export

        Returns:
            Any: the dataclass instance
        """
        entity = self.entity(dataclass_type.__name__)
        instance = dataclass_type(**entity.convert(record))
        return instance

    def view_ddl(
        self, view_db: str = "smartcrm_en", source_db: str = "smartcrm"
    ) -> str:
        """
        the DDL of all English views

        Args:
            view_db (str): the database holding the views
            source_db (str): the database holding the legacy tables

        Returns:
            str: the statements, one per entity
        """
        statements = [entity.view_ddl(view_db, source_db) for entity in self.tables()]
        ddl = "\n\n".join(statements) + "\n"
        return ddl

    def labels(self, lang: str = "en") -> Dict[str, str]:
        """
        the i18n labels in the given language

        Args:
            lang (str): en or de

        Returns:
            Dict[str, str]: <entity>_list for the plural of each table entity,
            <entity>.<field> for each field and the keys of the UI entity as they are
        """
        labels = {}
        for entity in self.entities.values():
            key_prefix = entity.name.lower()
            if entity.table:
                labels[f"{key_prefix}_list"] = entity.plural_label(lang)
                labels[key_prefix] = entity.de if lang == "de" else entity.en
            for field_spec in entity.fields.values():
                if entity.name == "UI":
                    labels[field_spec.name] = field_spec.label(lang)
                else:
                    labels[f"{key_prefix}.{field_spec.name}"] = field_spec.label(lang)
        return labels
