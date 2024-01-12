"""
Created on 2024-01-12

@author: wf
"""
import json

from ngwidgets.basetest import Basetest

from crm.crm_core import CRM, Organizations


class TestCRM(Basetest):
    """
    test CRM
    """

    def test_organizations(self):
        """ """
        org_lod = Organizations.from_json_file()
        debug = self.debug
        debug = True
        if debug:
            print(f"found {len(org_lod)} organizations")
            print(json.dumps(org_lod[0], indent=2,default=str))
