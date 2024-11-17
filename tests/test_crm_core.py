"""
Created on 2024-01-12

@author: wf
"""
import json
from typing import Dict, List

from ngwidgets.basetest import Basetest

from crm.smartcrm_adapter import SmartCRMAdapter, EntityType
from crm.crm_core import Organization, Person
from crm.db import DB

class TestCRM(Basetest):
    """
    test CRM
    """
    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.db = DB()
        # define entity types
        self.entity_types=[
            EntityType("Organisation", "organisations", Organization),
            EntityType("Person", "persons", Person)
        ]

    def show_lod(self, entity_type: EntityType, lod: List, limit: int = 3):
        if self.debug:
            print(f"found {len(lod)} {entity_type.plural_name}")
            for index in range(min(limit,len(lod))):
                print(json.dumps(lod[index], indent=2, default=str))

    def test_entities(self):
        """
        test reading entities
        """
        debug = self.debug
        debug = True
        for entity_type in self.entity_types:
            adapter = SmartCRMAdapter(entity_type)
            converter=lambda lod: [entity_type.dataclass.from_smartcrm(record) for record in lod]
            lod = adapter.from_json_file(converter=converter)
            self.show_lod(entity_type, lod)
            lod = adapter.from_db(self.db, converter=converter)
            self.show_lod(entity_type, lod)