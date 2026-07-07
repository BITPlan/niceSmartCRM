"""
Created on 2024-01-13

@author: wf
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from crm.crm_core import (
    Action,
    Contact,
    Email,
    Invoice,
    Organization,
    Person,
    Project,
    Todo,
)
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
    node_path: str  # e.g. OrganisationManager/organisations/Organisation
    pk_field: str = ""  # English dataclass field holding the primary key


class SmartCRMAdapter:
    """Generic adapter for SmartCRM entities"""

    def __init__(self, topic: smartCRMTopic):
        self.topic = topic

    @classmethod
    def get_topics(cls) -> List[smartCRMTopic]:
        # define entity types
        topics = [
            smartCRMTopic(
                name="Organization",
                plural_name="organizations",
                dataclass=Organization,
                table_name="organisation",
                node_path="OrganisationManager/organisations/Organisation",
                pk_field="organization_number",
            ),
            smartCRMTopic(
                name="Person",
                plural_name="persons",
                dataclass=Person,
                table_name="person",
                node_path="PersonManager/persons/Person",
                pk_field="person_number",
            ),
            smartCRMTopic(
                name="Contact",
                plural_name="contacts",
                dataclass=Contact,
                table_name="kontakt",
                node_path="KontaktManager/kontakts/Kontakt",
                pk_field="contact_number",
            ),
            smartCRMTopic(
                name="Invoice",
                plural_name="invoices",
                dataclass=Invoice,
                table_name="rechnung",
                node_path="RechnungManager/rechnungs/Rechnung",
                pk_field="invoice_id",
            ),
            smartCRMTopic(
                name="Email",
                plural_name="emails",
                dataclass=Email,
                table_name="email",
                node_path="EMailManager/emails/EMail",
                pk_field="email_id",
            ),
            smartCRMTopic(
                name="Project",
                plural_name="projects",
                dataclass=Project,
                table_name="projekt",
                node_path="ProjektManager/projekts/Projekt",
                pk_field="project_number",
            ),
            smartCRMTopic(
                name="Action",
                plural_name="actions",
                dataclass=Action,
                table_name="aktion",
                node_path="AktionManager/aktions/Aktion",
                pk_field="action_number",
            ),
            smartCRMTopic(
                name="Todo",
                plural_name="todos",
                dataclass=Todo,
                table_name="todo",
                node_path="TodoManager/todos/Todo",
                pk_field="todo_id",
            ),
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
            manager_name, plural_name, name = self.topic.node_path.split("/")

            # Use the components to access the data
            raw_lod = smartcrm_data[manager_name][plural_name][name]
            if converter:
                return converter(raw_lod)
            return raw_lod

    @staticmethod
    def root_path() -> str:
        """Get the root path dynamically based on home directory."""
        return str(Path.home() / ".smartcrm")
