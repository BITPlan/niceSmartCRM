"""
Created on 2024-01-12

@author: wf
"""
import json
from pathlib import Path
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import Dict, List, Optional

class EntityManager:
    @classmethod
    def _convert_to_datetime(cls,date_str: str) -> datetime:
        """
        Convert a string to a datetime object.
    
        Args:
            date_str (str): Date string to convert.
    
        Returns:
            datetime: A datetime object.
        """
        if date_str is None:
            return None
        parsed_date= datetime.fromisoformat(date_str) if date_str else None
        return parsed_date
    
    @classmethod
    def _convert_to_int(cls,num_str: str) -> int:
        """
        Convert a string to an integer.
    
        Args:
            num_str (str): Numeric string to convert.
    
        Returns:
            int: An integer value.
        """
        if num_str is None:
            return  None
        try:
            return int(num_str)
        except ValueError:
            return 0


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
    
    @classmethod
    def from_smartcrm(cls, smartcrm_org_lod: List[Dict]) -> List[Dict]:
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
                "created_at": cls._convert_to_datetime(org.get("createdAt")),
                "data_origin": org.get("DatenHerkunft"),
                "created_by": org.get("ErstelltVon"),
                "country": org.get("Land"),
                "last_modified": cls._convert_to_datetime(org.get("lastModified")),       
                "logo": org.get("logo", ""),
                "employee_count": cls._convert_to_int(org.get("Mitarbeiterzahl")),
                "organization_number": org.get("OrganisationNummer"),
                "city": org.get("Ort"),
                "postal_code": org.get("PLZ"),
                "po_box": org.get("Postfach"),
                "sales_estimate": cls._convert_to_int(org.get("salesEstimate")),
                "sales_rank": cls._convert_to_int(org.get("salesRank")),
                "location_name": org.get("Standort"),
                "phone": org.get("Telefon"),
                "revenue": cls._convert_to_int(org.get("Umsatz")),
                "revenue_probability": cls._convert_to_int(org.get("UmsatzWahrscheinlichkeit")),
                "revenue_potential": cls._convert_to_int(org.get("Umsatzpotential")),
                "country_dialing_code": org.get("VorwahlLand"),
                "city_dialing_code": org.get("VorwahlOrt"),
                "website": org.get("Web"),
                "importance": org.get("Wichtigkeit")
            }
            org_list.append(converted_org)
        return org_list

    @classmethod
    def from_json_file(cls, json_path: str=None):
        """
        read my lod from the given json_path
        """
        if json_path is None:
            json_path = f"{CRM.root_path()}/organisation.json"

        with open(json_path, "r") as json_file:
            org_data = json.load(json_file)
        smartcrm_org_lod = org_data["OrganisationManager"]["organisations"]["Organisation"]
        org_lod=cls.from_smartcrm(smartcrm_org_lod)
        return org_lod


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
