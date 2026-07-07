"""
Created on 2024-01-12

@author: wf
"""

import json
from pathlib import Path
from typing import List

from ngwidgets.basetest import Basetest

from crm.db import DB
from crm.smartcrm_adapter import SmartCRMAdapter, Topic


class TestCRM(Basetest):
    """
    test CRM
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        try:
            self.db = DB()
            self.db_error = None
        except Exception as ex:
            self.db = None
            self.db_error = ex

    def check_json_available(self):
        """Skip the current test if the smartcrm JSON exports are not available."""
        json_path = Path(SmartCRMAdapter.root_path()) / "organisation.json"
        if not json_path.is_file():
            self.skipTest(f"smartcrm JSON exports not available: {json_path}")

    def show_lod(self, topic: Topic, lod: List, limit: int = 1):
        if self.debug:
            print(f"found {len(lod)} {topic.plural_name}")
            for index in range(min(limit, len(lod))):
                print(json.dumps(lod[index], indent=2, default=str))

    def get_converter(self, topic: Topic):
        """Get a converter callback for the given topic."""
        converter = lambda lod: [
            topic.dataclass.from_smartcrm(record) for record in lod
        ]
        return converter

    def test_entities_from_json(self):
        """
        test reading and converting all entities from the JSON exports
        """
        self.check_json_available()
        min_counts = {
            "organizations": 100,
            "persons": 100,
            "contacts": 100,
            "invoices": 100,
            "emails": 100,
            "projects": 100,
            "actions": 100,
            "todos": 100,
        }
        for topic in SmartCRMAdapter.get_topics():
            adapter = SmartCRMAdapter(topic=topic)
            entities = adapter.from_json_file(converter=self.get_converter(topic))
            self.show_lod(topic, entities)
            min_count = min_counts[topic.plural_name]
            self.assertTrue(
                len(entities) >= min_count,
                f"expected at least {min_count} {topic.plural_name} - got {len(entities)}",
            )
            # every entity must convert and have its primary key set
            pk_missing = [
                entity for entity in entities if getattr(entity, topic.pk_field) is None
            ]
            self.assertEqual(
                len(pk_missing),
                0,
                f"{len(pk_missing)} {topic.plural_name} without {topic.pk_field}",
            )

    def test_entities_from_db(self):
        """
        test reading entities from the database
        """
        if self.db is None:
            self.skipTest(f"database not available: {self.db_error}")
        for topic in SmartCRMAdapter.get_topics():
            adapter = SmartCRMAdapter(topic=topic)
            entities = adapter.from_db(self.db, converter=self.get_converter(topic))
            self.show_lod(topic, entities)
            self.assertTrue(len(entities) > 0)
