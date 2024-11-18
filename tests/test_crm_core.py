"""
Created on 2024-01-12

@author: wf
"""
import json
from typing import Dict, List

from ngwidgets.basetest import Basetest

from crm.smartcrm_adapter import SmartCRMAdapter,Topic, smartCRMTopic
from crm.crm_core import Organization, Person, Contact
from crm.db import DB

class TestCRM(Basetest):
    """
    test CRM
    """
    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.db = DB()


    def show_lod(self, topic: Topic, lod: List, limit: int = 3):
        if self.debug:
            print(f"found {len(lod)} {topic.plural_name}")
            for index in range(min(limit,len(lod))):
                print(json.dumps(lod[index], indent=2, default=str))

    def test_entities(self):
        """
        test reading entities
        """
        debug = self.debug
        debug = True
        for topic in SmartCRMAdapter.get_topics():
            adapter = SmartCRMAdapter(topic=topic)
            converter=lambda lod: [topic.dataclass.from_smartcrm(record) for record in lod]
            lod = adapter.from_json_file(converter=converter)
            self.show_lod(topic, lod)
            lod = adapter.from_db(self.db, converter=converter)
            self.show_lod(topic, lod)