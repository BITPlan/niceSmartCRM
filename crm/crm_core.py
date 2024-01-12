"""
Created on 2024-01-12

@author: wf
"""
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dataclasses_json import dataclass_json


class EntityManager:
    """
    Generic Entity Manager
    """

    def __init__(self, entity_name: str, plural_name: str = None):
        self.entity_name = entity_name
        self.plural_name = plural_name if plural_name else f"{entity_name.lower()}s"
        # Handling first letter uppercase for JSON keys
        self.manager_name = (
            self.entity_name[0].upper() + self.entity_name[1:] + "Manager"
        )

    def _convert_to_datetime(self, date_str: str) -> datetime:
        """
        Convert a string to a datetime object.

        Args:
            date_str (str): Date string to convert.

        Returns:
            datetime: A datetime object.
        """
        if date_str is None:
            return None
        parsed_date = datetime.fromisoformat(date_str) if date_str else None
        return parsed_date

    def _convert_to_int(self, num_str: str) -> int:
        """
        Convert a string to an integer.

        Args:
            num_str (str): Numeric string to convert.

        Returns:
            int: An integer value.
        """
        if num_str is None:
            return None
        try:
            return int(num_str)
        except ValueError:
            return 0

    def from_json_file(self, json_path: str = None):
        """
        read my lod from the given json_path
        """
        if json_path is None:
            json_path = f"{CRM.root_path()}/{self.entity_name}.json"

        with open(json_path, "r") as json_file:
            smartcrm_data = json.load(json_file)
        # get the list of dicts
        smartcrm_lod = smartcrm_data[self.manager_name][self.plural_name][
            self.entity_name
        ]
        lod = self.from_smartcrm(smartcrm_lod)
        return lod


@dataclass_json
@dataclass
class Organization:
    kind: str
    industry: str
    created_at: datetime
    data_origin: str
    created_by: str
    country: str
    last_modified: datetime
    logo: str
    employee_count: int
    organization_number: str
    city: str
    postal_code: str
    po_box: str
    sales_estimate: int
    sales_rank: int
    location_name: str
    phone: str
    revenue: int
    revenue_probability: int
    revenue_potential: int
    country_dialing_code: str
    city_dialing_code: str
    website: str
    importance: str


class Organizations(EntityManager):
    """
    get organizations
    """

    def __init__(self):
        super().__init__(entity_name="Organisation")

    def from_smartcrm(self, smartcrm_org_lod: List[Dict]) -> List[Dict]:
        """
        Convert a list of organizations from the smartcrm_org_lod format to a list of dictionaries
        with appropriate field names and types.

        Args:
            smartcrm_org_lod (List[Dict]): List of organizations in smartcrm_org_lod format.

        Returns:
            List[Dict]: A list of dictionaries with converted field names and types.
        """
        org_list = []
        for org in smartcrm_org_lod:
            converted_org = {
                "kind": org.get("art"),
                "industry": org.get("Branche"),
                "created_at": self._convert_to_datetime(org.get("createdAt")),
                "data_origin": org.get("DatenHerkunft"),
                "created_by": org.get("ErstelltVon"),
                "country": org.get("Land"),
                "last_modified": self._convert_to_datetime(org.get("lastModified")),
                "logo": org.get("logo", ""),
                "employee_count": self._convert_to_int(org.get("Mitarbeiterzahl")),
                "organization_number": org.get("OrganisationNummer"),
                "city": org.get("Ort"),
                "postal_code": org.get("PLZ"),
                "po_box": org.get("Postfach"),
                "sales_estimate": self._convert_to_int(org.get("salesEstimate")),
                "sales_rank": self._convert_to_int(org.get("salesRank")),
                "location_name": org.get("Standort"),
                "phone": org.get("Telefon"),
                "revenue": self._convert_to_int(org.get("Umsatz")),
                "revenue_probability": self._convert_to_int(
                    org.get("UmsatzWahrscheinlichkeit")
                ),
                "revenue_potential": self._convert_to_int(org.get("Umsatzpotential")),
                "country_dialing_code": org.get("VorwahlLand"),
                "city_dialing_code": org.get("VorwahlOrt"),
                "website": org.get("Web"),
                "importance": org.get("Wichtigkeit"),
            }
            org_list.append(converted_org)
        return org_list


@dataclass_json
@dataclass
class Person:
    kind: str
    created_at: datetime
    data_origin: str
    email: str
    created_by: str
    comment: str
    last_modified: datetime
    name: str
    first_name: str
    personal: bool
    person_number: str
    sales_estimate: int
    sales_rank: int
    gender: str
    language: str
    subid: int


class Persons(EntityManager):
    def __init__(self):
        super().__init__(entity_name="Person")

    def from_smartcrm(self, smartcrm_person_lod: List[Dict]) -> List[Dict]:
        person_list = []
        for person in smartcrm_person_lod:
            converted_person = {
                "kind": person.get("Art"),
                "created_at": self._convert_to_datetime(person.get("createdAt")),
                "data_origin": person.get("DatenHerkunft"),
                "email": person.get("email"),
                "created_by": person.get("ErstelltVon"),
                "comment": person.get("Kommentar"),
                "last_modified": self._convert_to_datetime(person.get("lastModified")),
                "name": person.get("Name"),
                "first_name": person.get("Vorname"),
                "personal": person.get("perDu") == "true",
                "person_number": person.get("PersonNummer"),
                "sales_estimate": self._convert_to_int(person.get("salesEstimate")),
                "sales_rank": self._convert_to_int(person.get("salesRank")),
                "gender": person.get("sex"),
                "language": person.get("Sprache"),
                "subid": self._convert_to_int(person.get("subid")),
            }
            person_list.append(converted_person)
        return person_list


class CRM:
    """
    CRM
    """

    def __init__(self):
        pass

    @classmethod
    def root_path(cls) -> str:
        """
        Get the root path dynamically based on the home directory.
        """
        home = str(Path.home())
        # Append the relative path to the home directory
        root_path = f"{home}/.smartcrm"
        return root_path
