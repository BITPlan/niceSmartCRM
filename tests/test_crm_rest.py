"""
Created on 2026-07-07

@author: wf
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from ngwidgets.basetest import Basetest

from crm.crm_rest import CrmRestApi
from crm.smartcrm_adapter import SmartCRMAdapter


class TestCrmRestApi(Basetest):
    """
    test the read-only REST API
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        # use the JSON exports as data source - no database needed
        self.rest_api = CrmRestApi(db=None)
        self.app = FastAPI()
        self.app.include_router(self.rest_api.router)
        self.client = TestClient(self.app)

    def test_list_endpoints(self):
        """
        test the list endpoint for all topics
        """
        for topic in SmartCRMAdapter.get_topics():
            response = self.client.get(f"/api/{topic.plural_name}?limit=5")
            self.assertEqual(response.status_code, 200, topic.plural_name)
            lod = response.json()
            self.assertIsInstance(lod, list)
            self.assertTrue(len(lod) > 0, f"no {topic.plural_name} records")
            if self.debug:
                print(f"{topic.plural_name}: {len(lod)} records")

    def test_get_single_entity(self):
        """
        test getting a single entity by primary key for all topics
        """
        for topic in SmartCRMAdapter.get_topics():
            list_response = self.client.get(f"/api/{topic.plural_name}?limit=1")
            record = list_response.json()[0]
            entity_id = record[topic.pk_field]
            response = self.client.get(f"/api/{topic.plural_name}/{entity_id}")
            self.assertEqual(response.status_code, 200, topic.plural_name)
            entity = response.json()
            self.assertEqual(entity[topic.pk_field], entity_id)

    def test_not_found(self):
        """
        test 404 handling for unknown topics and ids
        """
        response = self.client.get("/api/unicorns")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/persons/no-such-id")
        self.assertEqual(response.status_code, 404)
