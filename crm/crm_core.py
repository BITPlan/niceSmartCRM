"""
Created on 2024-01-12

@author: wf
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from dataclasses_json import dataclass_json

from crm.em import EntityManager


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
