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
class Topic:
    """A generic entity / topic/ class description"""
    name: str
    plural_name: str
    dataclass: type

@dataclass
class smartCRMTopic(Topic):
    table_name: str
    node_path: str # e.g. OrganisationManager/organisations/Organisation

class SmartCRMAdapter:
    """Generic adapter for SmartCRM entities"""

    def __init__(self, topic: smartCRMTopic):
        self.topic=topic

    def from_db(self, db: DB, converter=None) -> List:
        """Fetch entities from database with optional conversion."""
        query = f"SELECT * FROM {self.topic.table_name}"
        raw_lod = db.execute_query(query)
        if converter:
            return converter(raw_lod)
        return raw_lod

    def from_json_file(self, json_path: str = None, converter=None) -> List:
        """Read entities from JSON file with optional conversion."""
        if json_path is None:
            json_path = f"{SmartCRMAdapter.root_path()}/{self.topic.table_name}.json"
        with open(json_path, "r") as json_file:
            smartcrm_data = json.load(json_file)
            # Split the node_path into its components
            manager_name, plural_name, name = self.topic.node_path.split('/')

            # Use the components to access the data
            raw_lod = smartcrm_data[manager_name][plural_name][name]
            if converter:
                return converter(raw_lod)
            return raw_lod

    @staticmethod
    def root_path() -> str:
        """Get the root path dynamically based on home directory."""
        return str(Path.home() / ".smartcrm")