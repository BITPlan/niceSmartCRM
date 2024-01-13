'''
Created on 2024-01-13

@author: wf
'''
from ngwidgets.basetest import Basetest
from linkml.person import Person
from linkml_runtime.dumpers import JSONDumper

class TestLinkML(Basetest):
    """
    test link ml generated classes
    
    """
    def test_person(self):
        p1 = Person(
            person_number="wf04002101",
            kind="contact"
        )
        if self.debug:
            print(p1)
        json_dumper=JSONDumper()
        if self.debug:
            print(json_dumper.dumps(p1))
