"""
Created on 2024-01-12

@author: wf
"""
import json

from ngwidgets.basetest import Basetest

from crm.crm_core import EntityManager, Organizations, Persons
from typing import Dict,List
from crm.db import DB

class TestCRM(Basetest):
    """
    test CRM
    """
    
    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.db=DB()
    
    def show_lod(self,entities:EntityManager,lod:List[Dict],limit:int=3):
        if self.debug:
            print(f"found {len(lod)} {entities.plural_name}")
            for index in range(limit):
                print(json.dumps(lod[index], indent=2, default=str))

    def test_entities(self):
        """
        test reading entities  
        """
        debug = self.debug
        debug = True
        for entity_class in (Organizations, Persons):
            entities = entity_class()
            lod = entities.from_json_file()
            self.show_lod(entities, lod)
            lod = entities.from_db(self.db)
            self.show_lod(entities,lod)
         