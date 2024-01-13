'''
Created on 2024-01-13

@author: wf
'''
from ngwidgets.basetest import Basetest
from crm.db import DB

class TestDB(Basetest):
    """
    test Database access layer
    """
    def test_db(self):
        # Usage example
        db = DB()
        results = db.execute_query("SELECT * FROM Person")
        for row in results:
            print(row)
