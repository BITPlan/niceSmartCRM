"""
Created on 2024-01-13

@author: wf
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from crm.db import DB


class CRM:
    """
    CRM
    """

    def __init__(self):
        pass

    @classmethod
    def root_path(cls) -> str:
        """
        Get the root path dynamically based on the home directory.
        """
        home = str(Path.home())
        # Append the relative path to the home directory
        root_path = f"{home}/.smartcrm"
        return root_path


class EntityManager:
    """
    Generic Entity Manager
    """

    def __init__(self, entity_name: str, plural_name: str = None):
        self.entity_name = entity_name
        self.plural_name = plural_name if plural_name else f"{entity_name.lower()}s"
        # Handling first letter uppercase for JSON keys
        self.manager_name = (
            self.entity_name[0].upper() + self.entity_name[1:] + "Manager"
        )

    def _convert_to_datetime(self, date_value: Any) -> datetime:
        """
        Convert a value to a datetime object.

        Args:
            date_str (Any): Date value to convert.

        Returns:
            datetime: A datetime object.
        """
        if date_value is None:
            return None
        if isinstance(date_value, str):
            date_str = date_value
            parsed_date = datetime.fromisoformat(date_str) if date_str else None
        else:
            parsed_date = date_value
        return parsed_date

    def _convert_to_int(self, num_str: str) -> int:
        """
        Convert a string to an integer.

        Args:
            num_str (str): Numeric string to convert.

        Returns:
            int: An integer value.
        """
        if num_str is None:
            return None
        try:
            return int(num_str)
        except ValueError:
            return 0

    def from_db(self, db: DB) -> List[Dict]:
        """
        Fetch entities from the database.

        Args:
            db (DB): Database object to execute queries.

        Returns:
            List[Dict]: A list of entity dictionaries.
        """
        query = f"SELECT * FROM {self.entity_name}"
        smartcrm_lod = db.execute_query(query)
        lod = self.from_smartcrm(smartcrm_lod)
        return lod

    def from_json_file(self, json_path: str = None):
        """
        read my lod from the given json_path
        """
        if json_path is None:
            json_path = f"{CRM.root_path()}/{self.entity_name}.json"

        with open(json_path, "r") as json_file:
            smartcrm_data = json.load(json_file)
        # get the list of dicts
        smartcrm_lod = smartcrm_data[self.manager_name][self.plural_name][
            self.entity_name
        ]
        lod = self.from_smartcrm(smartcrm_lod)
        return lod
