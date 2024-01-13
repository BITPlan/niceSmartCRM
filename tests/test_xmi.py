"""
Created on 2024-01-13

@author: wf
"""

from crm.xmi import Model
from ngwidgets.basetest import Basetest
from pathlib import Path

class TestXMI(Basetest):
    """
    test reading XMI
    """

    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.xmi_json_path=f"{Path.home()}/.smartcrm/smartcrm_model.json"
        
    def test_raw_read_xmi(self):
        """
        test reading xmi file
        """
        data=Model.raw_read_xmi_json(self.xmi_json_path)
        if self.debug:
            pass
        pass
    
    def test_xmi_from_xmi_json(self):
        """
        test reading xmi file to XMI struture
        """
        model=Model.from_xmi_json(self.xmi_json_path)
        plant_uml=model.to_plant_uml()
        if self.debug:
            print(plant_uml)
        pass
        