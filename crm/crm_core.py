"""
Created on 2024-01-12

@author: wf
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, TypeVar

T = TypeVar("T")


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

    @staticmethod
    def to_bool(value: Any) -> Optional[bool]:
        """Convert a value to a boolean.

        Handles the legacy string representation ("true"/"false") from
        JSON/XML exports as well as int/bool values from the database.
        """
        result = None
        if value is not None:
            if isinstance(value, bool):
                result = value
            elif isinstance(value, int):
                result = value != 0
            else:
                result = str(value).lower() in ("true", "1", "yes")
        return result

    @staticmethod
    def to_float(value: Any) -> Optional[float]:
        """Convert a value to a float."""
        result = None
        if value is not None:
            try:
                result = float(value)
            except (ValueError, TypeError):
                result = None
        return result


@dataclass
class Organization:
    name: Optional[str]  # Name
    street: Optional[str]  # Strasse
    fax: Optional[str]  # Telefax
    comment: Optional[str]  # Kommentar
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
    def from_smartcrm(cls, data: Dict) -> "Organization":
        """Convert SmartCRM data dictionary to Organization instance."""
        return cls(
            name=data.get("Name"),
            street=data.get("Strasse"),
            fax=data.get("Telefax"),
            comment=data.get("Kommentar"),
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
            revenue_probability=TypeConverter.to_int(
                data.get("UmsatzWahrscheinlichkeit")
            ),
            revenue_potential=TypeConverter.to_int(data.get("Umsatzpotential")),
            country_dialing_code=data.get("VorwahlLand"),
            city_dialing_code=data.get("VorwahlOrt"),
            website=data.get("Web"),
            importance=data.get("Wichtigkeit"),
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
    other_email: Optional[str] = None  # otheremail
    phone: Optional[str] = None  # Telefon
    fax: Optional[str] = None  # Telefax
    mobile: Optional[str] = None  # Mobiltelefon
    social_links: Optional[str] = None  # socialLinks
    photo: Optional[str] = None
    salutation: Optional[str] = None  # Anrede
    title: Optional[str] = None  # Titel
    academic_title: Optional[str] = None  # akademischerTitel
    private_street: Optional[str] = None  # StrassePrivat
    private_postal_code: Optional[str] = None  # PLZPrivat
    private_city: Optional[str] = None  # OrtPrivat
    responsible: Optional[str] = None  # Sachbearbeiter
    organization_number: Optional[str] = None  # meineOrganisation_OrganisationNummer

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Person":
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
            personal=TypeConverter.to_bool(data.get("perDu")),
            person_number=data.get("PersonNummer"),
            sales_estimate=TypeConverter.to_int(data.get("salesEstimate")),
            sales_rank=TypeConverter.to_int(data.get("salesRank")),
            gender=data.get("sex"),
            language=data.get("Sprache"),
            subid=TypeConverter.to_int(data.get("subid")),
            other_email=data.get("otheremail"),
            phone=data.get("Telefon"),
            fax=data.get("Telefax"),
            mobile=data.get("Mobiltelefon"),
            social_links=data.get("socialLinks"),
            photo=data.get("photo"),
            salutation=data.get("Anrede"),
            title=data.get("Titel"),
            academic_title=data.get("akademischerTitel"),
            private_street=data.get("StrassePrivat"),
            private_postal_code=data.get("PLZPrivat"),
            private_city=data.get("OrtPrivat"),
            responsible=data.get("Sachbearbeiter"),
            organization_number=data.get("meineOrganisation_OrganisationNummer"),
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
    def from_smartcrm(cls, data: Dict) -> "Contact":
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
            created_at=data.get("createdAt"),
        )


@dataclass
class Invoice:
    invoice_id: str
    organization_number: Optional[str]
    comment: Optional[str]
    paid_at: Optional[datetime]
    gross_amount: Optional[float]
    deleted_at: Optional[datetime]
    created_by: Optional[str]
    last_modified: Optional[datetime]
    net_amount: Optional[float]
    invoice_date: Optional[datetime]
    invoice_number: Optional[str]
    year_assignment: Optional[str]
    month_assignment: Optional[str]
    project_number: Optional[str]
    division: Optional[str]
    payment_statement: Optional[str]
    document: Optional[str]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Invoice":
        """Convert SmartCRM data dictionary to Invoice instance."""
        return cls(
            invoice_id=data.get("rechnungsID"),
            organization_number=data.get("Auftraggeber_OrganisationNummer"),
            comment=data.get("bemerkung"),
            paid_at=TypeConverter.to_datetime(data.get("bezahltAm")),
            gross_amount=data.get("brutto"),
            deleted_at=TypeConverter.to_datetime(data.get("deletedAt")),
            created_by=data.get("erstelltVon"),
            last_modified=TypeConverter.to_datetime(data.get("lastmodified")),
            net_amount=data.get("netto"),
            invoice_date=TypeConverter.to_datetime(data.get("rechnungsdatum")),
            invoice_number=data.get("rechnungsnummer"),
            year_assignment=data.get("zuordnungJahr"),
            month_assignment=data.get("zuordnungMonat"),
            project_number=data.get("ZuordnungProjekt_ProjektNummer"),
            division=data.get("zuordnungSparte"),
            payment_statement=data.get("bezahltAuszug"),
            document=data.get("document"),
        )


@dataclass
class Email:
    """An email record"""

    email_id: str  # EMailId
    to_address: Optional[str]  # ToAdr
    cc: Optional[str]  # CC
    bcc: Optional[str]  # BCC
    reply_to: Optional[str]  # ReplyTo
    subject: Optional[str]  # Subject
    content: Optional[str]  # Content
    signature: Optional[str]
    attachment: Optional[str]  # Attachment
    pegasus_id: Optional[str]  # PegasusId
    sent: Optional[bool]
    send_date: Optional[datetime]  # sendDate
    uid: Optional[str]
    deleted_at: Optional[datetime]
    last_modified: Optional[datetime]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Email":
        """Convert SmartCRM data dictionary to Email instance."""
        return cls(
            email_id=data.get("EMailId"),
            to_address=data.get("ToAdr"),
            cc=data.get("CC"),
            bcc=data.get("BCC"),
            reply_to=data.get("ReplyTo"),
            subject=data.get("Subject"),
            content=data.get("Content"),
            signature=data.get("signature"),
            attachment=data.get("Attachment"),
            pegasus_id=data.get("PegasusId"),
            sent=TypeConverter.to_bool(data.get("sent")),
            send_date=TypeConverter.to_datetime(data.get("sendDate")),
            uid=data.get("uid"),
            deleted_at=TypeConverter.to_datetime(data.get("deletedAt")),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
        )


@dataclass
class Project:
    """A project"""

    project_number: str  # ProjektNummer
    name: Optional[str]
    year: Optional[str]  # jahr
    customer_order_number: Optional[str]  # auftragsnrkunde
    status: Optional[str]
    goals: Optional[str]  # ziele
    goal_achievement: Optional[str]  # zielerrreichungsgrad
    documentation: Optional[str]  # dokumentation
    planned_start: Optional[datetime]  # plananfang
    planned_end: Optional[datetime]  # planende
    planned_effort: Optional[int]  # planaufwand
    planned_cost: Optional[int]  # plankosten
    actual_start: Optional[datetime]  # istanfang
    actual_end: Optional[datetime]  # istende
    actual_effort: Optional[int]  # istaufwand
    actual_cost: Optional[int]  # istkosten
    last_modified: Optional[datetime]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Project":
        """Convert SmartCRM data dictionary to Project instance."""
        return cls(
            project_number=data.get("ProjektNummer"),
            name=data.get("name"),
            year=data.get("jahr"),
            customer_order_number=data.get("auftragsnrkunde"),
            status=data.get("status"),
            goals=data.get("ziele"),
            goal_achievement=data.get("zielerrreichungsgrad"),
            documentation=data.get("dokumentation"),
            planned_start=TypeConverter.to_datetime(data.get("plananfang")),
            planned_end=TypeConverter.to_datetime(data.get("planende")),
            planned_effort=TypeConverter.to_int(data.get("planaufwand")),
            planned_cost=TypeConverter.to_int(data.get("plankosten")),
            actual_start=TypeConverter.to_datetime(data.get("istanfang")),
            actual_end=TypeConverter.to_datetime(data.get("istende")),
            actual_effort=TypeConverter.to_int(data.get("istaufwand")),
            actual_cost=TypeConverter.to_int(data.get("istkosten")),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
        )


@dataclass
class Action:
    """An action/campaign"""

    action_number: str  # AktionNummer
    name: Optional[str]
    topic: Optional[str]  # Thema
    date: Optional[datetime]  # Datum
    contact_type: Optional[str]  # Kontaktart
    contact_person: Optional[str]  # Ansprechpartner
    comment: Optional[str]  # kommentar
    copy_contents: Optional[bool]  # inhalteKopieren
    deleted_at: Optional[datetime]
    last_modified: Optional[datetime]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Action":
        """Convert SmartCRM data dictionary to Action instance."""
        return cls(
            action_number=data.get("AktionNummer"),
            name=data.get("name"),
            topic=data.get("Thema"),
            date=TypeConverter.to_datetime(data.get("Datum")),
            contact_type=data.get("Kontaktart"),
            contact_person=data.get("Ansprechpartner"),
            comment=data.get("kommentar"),
            copy_contents=TypeConverter.to_bool(data.get("inhalteKopieren")),
            deleted_at=TypeConverter.to_datetime(data.get("deletedAt")),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
        )


@dataclass
class Todo:
    """A todo item"""

    todo_id: str  # id
    task: Optional[str]  # aufgabe
    creator: Optional[str]  # ersteller
    created_on: Optional[datetime]  # erstellungsdatum
    responsible: Optional[str]  # verantwortlicher
    accepted: Optional[bool]  # akzeptiert
    accepted_at: Optional[datetime]  # akzeptiertAm
    importance: Optional[str]  # wichtigkeit
    urgency: Optional[str]  # dringlichkeit
    planned_date: Optional[datetime]  # plantermin
    completed_at: Optional[datetime]  # erledigtAm
    status: Optional[str]
    deleted_at: Optional[datetime]
    last_modified: Optional[datetime]

    @classmethod
    def from_smartcrm(cls, data: Dict) -> "Todo":
        """Convert SmartCRM data dictionary to Todo instance."""
        return cls(
            todo_id=data.get("id"),
            task=data.get("aufgabe"),
            creator=data.get("ersteller"),
            created_on=TypeConverter.to_datetime(data.get("erstellungsdatum")),
            responsible=data.get("verantwortlicher"),
            accepted=TypeConverter.to_bool(data.get("akzeptiert")),
            accepted_at=TypeConverter.to_datetime(data.get("akzeptiertAm")),
            importance=data.get("wichtigkeit"),
            urgency=data.get("dringlichkeit"),
            planned_date=TypeConverter.to_datetime(data.get("plantermin")),
            completed_at=TypeConverter.to_datetime(data.get("erledigtAm")),
            status=data.get("status"),
            deleted_at=TypeConverter.to_datetime(data.get("deletedAt")),
            last_modified=TypeConverter.to_datetime(data.get("lastModified")),
        )
