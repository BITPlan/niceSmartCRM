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
        try:
            self.db = DB()
            self.db_error = None
        except Exception as ex:
            self.db = None
            self.db_error = ex

    def check_db_available(self):
        """Skip the current test if the database is not available."""
        if self.db is None:
            self.skipTest(f"database not available: {self.db_error}")

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
        self.check_db_available()
        limit = 3
        _results = self.check_query(f"SELECT * FROM person LIMIT {limit}", limit)
        _results = self.check_query(
            f"SELECT * FROM person WHERE personnummer='wf04002101'", expected=1
        )

    def test_show_tables(self):
        """
        test showing all tables
        """
        self.check_db_available()
        results = self.check_query("SHOW TABLES", 25)
        if self.debug:
            print(results)
