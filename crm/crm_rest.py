"""
Created on 2026-07-07

@author: wf
"""

from dataclasses import asdict
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

from crm.db import DB
from crm.smartcrm_adapter import SmartCRMAdapter, smartCRMTopic


class CrmRestApi:
    """
    Read-only REST API for the smartCRM entities.

    Provides English-named endpoints for all topics registered in
    SmartCRMAdapter, e.g. /api/organizations and /api/organizations/{id}.
    Records are read via the anti-corruption layer from the shared MariaDB
    smartcrm database or - as a fallback - from the JSON exports in
    ~/.smartcrm.
    """

    def __init__(self, db: Optional[DB] = None):
        """
        Initialize the REST API.

        Args:
            db (Optional[DB]): database connection; if None the JSON export
                               files are used as data source
        """
        self.db = db
        self.topics: Dict[str, smartCRMTopic] = {
            topic.plural_name: topic for topic in SmartCRMAdapter.get_topics()
        }
        self.cache: Dict[str, List[Any]] = {}
        self.router = APIRouter(prefix="/api", tags=["smartCRM"])
        self.register_routes()

    def get_topic(self, plural_name: str) -> smartCRMTopic:
        """
        Get the topic for the given plural name.

        Args:
            plural_name (str): the plural entity name e.g. "organizations"

        Returns:
            smartCRMTopic: the matching topic

        Raises:
            HTTPException: 404 if the topic is unknown
        """
        topic = self.topics.get(plural_name)
        if topic is None:
            raise HTTPException(
                status_code=404, detail=f"unknown entity type: {plural_name}"
            )
        return topic

    def get_records(self, topic: smartCRMTopic) -> List[Any]:
        """
        Get the converted dataclass records for the given topic.

        Records are cached after the first read since the API is read-only.

        Args:
            topic (smartCRMTopic): the topic to read records for

        Returns:
            List[Any]: list of dataclass instances
        """
        records = self.cache.get(topic.plural_name)
        if records is None:
            adapter = SmartCRMAdapter(topic=topic)
            converter = lambda lod: [
                topic.dataclass.from_smartcrm(record) for record in lod
            ]
            if self.db is not None:
                records = adapter.from_db(self.db, converter=converter)
            else:
                records = adapter.from_json_file(converter=converter)
            self.cache[topic.plural_name] = records
        return records

    def register_routes(self):
        """
        Register the list and single-entity routes on the router.
        """

        @self.router.get("/{plural_name}")
        def list_entities(
            plural_name: str, limit: int = 100, offset: int = 0
        ) -> List[Dict]:
            """List entities of the given type."""
            topic = self.get_topic(plural_name)
            records = self.get_records(topic)
            lod = [asdict(record) for record in records[offset : offset + limit]]
            return lod

        @self.router.get("/{plural_name}/{entity_id}")
        def get_entity(plural_name: str, entity_id: str) -> Dict:
            """Get a single entity by its primary key."""
            topic = self.get_topic(plural_name)
            records = self.get_records(topic)
            for record in records:
                if getattr(record, topic.pk_field, None) == entity_id:
                    record_dict = asdict(record)
                    return record_dict
            raise HTTPException(
                status_code=404,
                detail=f"no {topic.name} with {topic.pk_field}={entity_id}",
            )
