"""
Created on 2024-01-13


@author: wf
"""
from pathlib import Path
from typing import Any, Dict, List

import pymysql
import yaml


class DB:
    """
    Database wrapper for managing direct database connections and executing queries using PyMySQL.

    Attributes:
        config (Dict[str, Any]): Database configuration details.
        connection (pymysql.connections.Connection): PyMySQL connection instance.
    """

    def __init__(self, config_path: str = None):
        """
        Initializes the database connection using provided configuration.

        Args:
            config_path (str, optional): Path to the configuration YAML file.
                                         Defaults to '~/.smartcrm/db_config.yaml'.
        """
        if config_path is None:
            config_path = f"{Path.home()}/.smartcrm/db_config.yaml"
        self.config = self.load_config(config_path)
        self.connection = self.create_connection()

    def load_config(self, path: str) -> Dict[str, Any]:
        """
        Loads the database configuration from a YAML file.

        Args:
            path (str): The file path of the YAML configuration file.

        Returns:
            Dict[str, Any]: A dictionary containing database configuration.
        """
        with open(path, "r") as file:
            return yaml.safe_load(file)["database"]

    def create_connection(self) -> pymysql.connections.Connection:
        """
        Creates a PyMySQL connection using the loaded configuration.

        Returns:
            pymysql.connections.Connection: PyMySQL connection instance.
        """
        config = {
            "host": self.config["host"],
            "user": self.config["user"],
            "password": self.config["password"],
            "db": self.config["name"],
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
        }
        return pymysql.connect(**config)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a SQL query and returns the results.

        Args:
            query (str): The SQL query to execute.

        Returns:
            List[Dict[str, Any]]: The result of the SQL query execution.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
