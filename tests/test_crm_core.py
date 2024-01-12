"""
Created on 2024-01-12

@author: wf
"""
import json

from ngwidgets.basetest import Basetest

from crm.crm_core import CRM, Organizations, Persons


class TestCRM(Basetest):
    """
    test CRM
    """

    def test_entities(self):
        """ """
        debug = self.debug
        debug = True
        for entity_class in (Organizations, Persons):
            entities = entity_class()
            lod = entities.from_json_file()
            if debug:
                print(f"found {len(lod)} {entities.plural_name}")
                print(json.dumps(lod[0], indent=2, default=str))
