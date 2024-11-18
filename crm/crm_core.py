"""
Created on 2024-01-12

@author: wf
"""
from datetime import datetime
from typing import Dict, Any, TypeVar, Optional
from dataclasses import dataclass

T = TypeVar('T')

class TypeConverter:
    """Helper class for type conversions"""

    @staticmethod
    def to_datetime(date_value: Any) -> Optional[datetime]:
        """Convert a value to a datetime object."""
        if date_value is None:
            return None
        if isinstance(date_value, str):
            return datetime.fromisoformat(date_value) if date_value else None
        return date_value

    @staticmethod
    def to_int(num_str: str) -> Optional[int]:
        """Convert a string to an integer."""
        if num_str is None:
            return None
        try:
            return int(num_str)
        except ValueError:
            return 0

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

    @classmethod
    def from_smartcrm(cls, data: Dict) -> 'Organization':
        """Convert SmartCRM data dictionary to Organization instance."""
        return cls(
            kind=data.get("art"),
            industry=data.get("Branche"),
            created_at=TypeConverter.to_datetime(data.get("createdAt")),
            data_origin=data.get("DatenHerkunft"),
            created_by=data.get("ErstelltVon"),
            country=data.get("Land"),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
            logo=data.get("logo", ""),
            employee_count=TypeConverter.to_int(data.get("Mitarbeiterzahl")),
            organization_number=data.get("OrganisationNummer"),
            city=data.get("Ort"),
            postal_code=data.get("PLZ"),
            po_box=data.get("Postfach"),
            sales_estimate=TypeConverter.to_int(data.get("salesEstimate")),
            sales_rank=TypeConverter.to_int(data.get("salesRank")),
            location_name=data.get("Standort"),
            phone=data.get("Telefon"),
            revenue=TypeConverter.to_int(data.get("Umsatz")),
            revenue_probability=TypeConverter.to_int(data.get("UmsatzWahrscheinlichkeit")),
            revenue_potential=TypeConverter.to_int(data.get("Umsatzpotential")),
            country_dialing_code=data.get("VorwahlLand"),
            city_dialing_code=data.get("VorwahlOrt"),
            website=data.get("Web"),
            importance=data.get("Wichtigkeit")
        )

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

    @classmethod
    def from_smartcrm(cls, data: Dict) -> 'Person':
        """Convert SmartCRM data dictionary to Person instance."""
        return cls(
            kind=data.get("Art"),
            created_at=TypeConverter.to_datetime(data.get("createdAt")),
            data_origin=data.get("DatenHerkunft"),
            email=data.get("email"),
            created_by=data.get("ErstelltVon"),
            comment=data.get("Kommentar"),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
            name=data.get("Name"),
            first_name=data.get("Vorname"),
            personal=data.get("perDu") == "true",
            person_number=data.get("PersonNummer"),
            sales_estimate=TypeConverter.to_int(data.get("salesEstimate")),
            sales_rank=TypeConverter.to_int(data.get("salesRank")),
            gender=data.get("sex"),
            language=data.get("Sprache"),
            subid=TypeConverter.to_int(data.get("subid"))
        )

@dataclass
class Contact:
    """A CRM contact"""
    contact_number: str  # KontaktNummer
    email_id: Optional[str]  # eMail_EMailId
    active: Optional[str]  # aktiv
    contact_person: Optional[str]  # Ansprechpartner
    attachment: Optional[str]
    date: Optional[datetime]  # Datum
    deleted_at: Optional[datetime]
    completed: Optional[datetime]  # erledigt
    comment: Optional[str]  # Kommentar
    contact_type: Optional[str]  # Kontaktart
    last_modified: Optional[datetime]
    person_number: Optional[str]  # meinePerson_PersonNummer
    topic: Optional[str]  # Thema
    todo: Optional[str]
    uid: Optional[str]
    responsible: Optional[str]  # Verantwortlicher
    action_number: Optional[str]  # wgAktion_AktionNummer
    followup: Optional[datetime]  # Wiedervorlage
    created_at: Optional[datetime]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> 'Contact':
        """Convert SmartCRM data to Contact instance"""
        return cls(
            contact_number=data.get("KontaktNummer"),
            email_id=data.get("eMail_EMailId"),
            active=data.get("aktiv"),
            contact_person=data.get("Ansprechpartner"),
            attachment=data.get("attachment"),
            date=data.get("Datum"),
            deleted_at=data.get("deletedAt"),
            completed=data.get("erledigt"),
            comment=data.get("Kommentar"),
            contact_type=data.get("Kontaktart"),
            last_modified=data.get("lastmodified"),
            person_number=data.get("meinePerson_PersonNummer"),
            topic=data.get("Thema"),
            todo=data.get("todo"),
            uid=data.get("uid"),
            responsible=data.get("Verantwortlicher"),
            action_number=data.get("wgAktion_AktionNummer"),
            followup=data.get("Wiedervorlage"),
            created_at=data.get("createdAt")
        )