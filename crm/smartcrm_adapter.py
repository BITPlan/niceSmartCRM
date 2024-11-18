"""
Created on 2024-01-13

@author: wf
"""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
from crm.db import DB
from crm.crm_core import Organization, Person, Contact

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

    @classmethod
    def get_topics(cls)->List[smartCRMTopic]:
        # define entity types
        topics = [
            smartCRMTopic(
                name="Organization",
                plural_name="organizations",
                dataclass=Organization,
                table_name="Organisation",
                node_path="OrganisationManager/organisations/Organisation",
            ),
            smartCRMTopic(
                name="Person",
                plural_name="persons",
                dataclass=Person,
                table_name="Person",
                node_path="PersonManager/persons/Person",
            ),
            smartCRMTopic(
                name="Contact",
                plural_name="contacts",
                dataclass=Contact,
                table_name="Kontakt",
                node_path="KontaktManager/kontakts/Kontakt",
            )
        ]
        return topics

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