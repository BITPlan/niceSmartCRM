"""
Created on 2026-09-23

@author: wf
"""

from dataclasses import fields as dataclass_fields

import i18n
from ngwidgets.basetest import Basetest

from crm.db import DB
from crm.fields import Fields
from crm.i18n_config import I18nConfig
from crm.smartcrm_adapter import SmartCRMAdapter


class TestFields(Basetest):
    """
    test the field descriptors of fields.yaml
    """

    view_db = "test_smartcrm_en"

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.fields = Fields.get()
        try:
            self.db = DB()
            self.db_error = None
        except Exception as ex:
            self.db = None
            self.db_error = ex

    def check_db_available(self):
        """Skip the current test if the database is not available."""
        if self.db is None:
            self.skipTest(f"database not available: {self.db_error}")

    def test_covers_dataclasses(self):
        """
        every topic has an entity spec whose fields are exactly the dataclass fields,
        with the topic's table and primary key
        """
        for topic in SmartCRMAdapter.get_topics():
            entity = self.fields.entity(topic.name)
            dc_names = {f.name for f in dataclass_fields(topic.dataclass)}
            self.assertEqual(dc_names, set(entity.fields.keys()), topic.name)
            self.assertEqual(topic.table_name, entity.table)
            self.assertEqual(topic.plural_name, entity.plural)
            self.assertEqual(topic.pk_field, entity.pk.name)

    def test_columns_exist(self):
        """
        every column of fields.yaml is a column of its legacy table
        """
        self.check_db_available()
        for entity in self.fields.tables():
            rows = self.db.execute_query(
                "SELECT column_name FROM information_schema.columns "
                f"WHERE table_schema=DATABASE() AND table_name='{entity.table}'"
            )
            columns = {row["column_name"] for row in rows}
            for field_spec in entity.fields.values():
                self.assertIn(
                    field_spec.column, columns, f"{entity.name}.{field_spec.name}"
                )

    def test_convert(self):
        """
        conversion of a legacy row and of a JAXB export record give the same instance
        """
        person = self.fields.entity("Person").fields
        db_row = {
            "PersonNummer": "wf04005638",
            "Vorname": "Rhett",
            "salesrank": 3,
            "perDu": 0,
        }
        json_record = {
            "PersonNummer": "wf04005638",
            "Vorname": "Rhett",
            "salesRank": "3",
            "perDu": "false",
        }
        for record in [db_row, json_record]:
            self.assertEqual("wf04005638", person["person_number"].convert(record))
            self.assertEqual("Rhett", person["first_name"].convert(record))
            self.assertEqual(3, person["sales_rank"].convert(record))
            self.assertEqual(False, person["personal"].convert(record))
        # the reference of the foreign key
        self.assertEqual("Organization", person["organization_number"].reference)
        self.assertEqual(
            "", self.fields.entity("Organization").fields["logo"].convert({})
        )

    def test_view_ddl(self):
        """
        the English views are generated for all table entities and, with a database, apply
        """
        ddl = self.fields.view_ddl(view_db=self.view_db)
        if self.debug:
            print(ddl)
        for entity in self.fields.tables():
            self.assertIn(f"`{self.view_db}`.`{entity.view_name()}`", ddl)
        self.assertIn("`Vorname` AS `first_name`", ddl)
        self.check_db_available()
        self.db.execute_query(f"CREATE DATABASE IF NOT EXISTS `{self.view_db}`")
        for statement in ddl.split(";\n"):
            if statement.strip():
                self.db.execute_query(statement)
        rows = self.db.execute_query(
            f"SELECT first_name, organization_number FROM `{self.view_db}`.`person` "
            "WHERE person_number='wf04002101'"
        )
        self.assertEqual(1, len(rows))
        self.assertIn("first_name", rows[0])

    def test_labels(self):
        """
        the i18n labels come from fields.yaml in both languages
        """
        en = self.fields.labels("en")
        de = self.fields.labels("de")
        self.assertEqual("Persons", en["person_list"])
        self.assertEqual("Personen", de["person_list"])
        self.assertEqual("First Name", en["person.first_name"])
        self.assertEqual("Vorname", de["person.first_name"])
        self.assertEqual("Knoten", de["nodetypeconfig_list"])
        I18nConfig.config(debug=self.debug)
        i18n.set("locale", "de")
        self.assertEqual("Organisationen", i18n.t("organization_list"))
        i18n.set("locale", "en")
        self.assertEqual("Organizations", i18n.t("organization_list"))
