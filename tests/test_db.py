"""
Created on 2024-01-13

@author: wf
"""
import json

from ngwidgets.basetest import Basetest

from crm.db import DB

class TestDB(Basetest):
    """
    test Database access layer
    """

    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.db = DB()

    def check_query(self, sql_query, expected):
        results = self.db.execute_query(sql_query)
        if self.debug:
            for row in results:
                row_str = json.dumps(row, indent=2, default=str)
                print(row_str)
        self.assertTrue(len(results) >= expected)
        return results

    def test_db(self):
        """
        test database access
        """
        limit = 3
        _results = self.check_query(f"SELECT * FROM person LIMIT {limit}", limit)
        _results = self.check_query(
            f"SELECT * FROM person WHERE personnummer='wf04002101'", expected=1
        )

    def test_show_tables(self):
        """
        test showing all tables
        """
        results = self.check_query("SHOW TABLES", 25)
        if self.debug:
            print(results)
