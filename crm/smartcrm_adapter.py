"""
Created on 2024-01-13

@author: wf
"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
from crm.db import DB

@dataclass
class EntityType:
    """A generic entity description"""
    name: str
    plural_name: str
    dataclass: type

    @property
    def manager_name(self) -> str:
        """Get the manager name for this entity"""
        return f"{self.name[0].upper()}{self.name[1:]}Manager"

class SmartCRMAdapter:
    """Generic adapter for SmartCRM entities"""

    def __init__(self, entity_type: EntityType):
        self.et = entity_type

    def from_db(self, db: DB, converter=None) -> List:
        """Fetch entities from database with optional conversion."""
        query = f"SELECT * FROM {self.et.name}"
        raw_lod = db.execute_query(query)
        if converter:
            return converter(raw_lod)
        return raw_lod

    def from_json_file(self, json_path: str = None, converter=None) -> List:
        """Read entities from JSON file with optional conversion."""
        if json_path is None:
            json_path = f"{SmartCRMAdapter.root_path()}/{self.et.name}.json"
        with open(json_path, "r") as json_file:
            smartcrm_data = json.load(json_file)
            raw_lod = smartcrm_data[self.et.manager_name][self.et.plural_name][self.et.name]
            if converter:
                return converter(raw_lod)
            return raw_lod

    @staticmethod
    def root_path() -> str:
        """Get the root path dynamically based on home directory."""
        return str(Path.home() / ".smartcrm")