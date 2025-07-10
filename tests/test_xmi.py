"""
Created on 2024-01-13

@author: wf
"""

from pathlib import Path

from ngwidgets.basetest import Basetest

from crm.xmi import Model


class TestXMI(Basetest):
    """
    test reading XMI
    """

    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.xmi_json_path = f"{Path.home()}/.smartcrm/smartcrm_model.json"

    def test_raw_read_xmi(self):
        """
        test reading xmi file
        """
        data = Model.raw_read_xmi_json(self.xmi_json_path)
        if self.debug:
            pass
        pass

    def test_xmi_from_xmi_json(self):
        """
        test reading xmi file to XMI structure
        """
        model = Model.from_xmi_json(self.xmi_json_path)
        verbose = False
        if self.debug:
            print(f"found {len(model.lookup)} model elements")
            if verbose:
                for model_id, element in model.lookup.items():
                    print(
                        f"{model_id}:{element.__class__.__name__}:{element.short_name}"
                    )
        plant_uml = model.to_plant_uml()
        xmi_json = model.to_json(indent=2)
        for file_path, text in [
            ("/tmp/smartcrm.puml", plant_uml),
            ("/tmp/smartcrm_xmi.json", xmi_json),
        ]:
            with open(file_path, "w") as output_file:
                output_file.write(text)
