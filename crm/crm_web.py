"""
Created on 2024-01-10

@author: wf
"""
from ngwidgets.input_webserver import InputWebserver
from ngwidgets.lod_grid import ListOfDictsGrid
from ngwidgets.progress import NiceguiProgressbar
from ngwidgets.webserver import WebserverConfig
from nicegui import Client, app, ui

from crm.crm_core import CRM, Organizations, Persons
from crm.version import Version


class CrmWebServer(InputWebserver):
    """
    server for self-assessment
    """

    @classmethod
    def get_config(cls) -> WebserverConfig:
        """
        get the configuration for this Webserver
        """
        copy_right = "(c)2024 Wolfgang Fahl"
        config = WebserverConfig(
            copy_right=copy_right, version=Version(), default_port=9854
        )
        return config

    def __init__(self):
        """Constructs all the necessary attributes for the WebServer object."""
        InputWebserver.__init__(self, config=CrmWebServer.get_config())
        self.load_entities()
        
        @ui.page("/organizations")
        async def organizations(client: Client):
            return await self.organizations()

        @ui.page("/persons")
        async def persons(client: Client):
            return await self.persons()
        
        
    def load_entities(self):
        organizations=Organizations()
        self.org_lod = organizations.from_json_file()
        persons=Persons()
        self.person_lod = persons.from_json_file()

    def configure_menu(self):
        """
        configure the menu
        """
        self.link_button(
            name="organizations", 
            icon_name="apartment", 
            target="/organizations"
        )
        self.link_button(
            name="persons", 
            icon_name="people", 
            target="/persons"
        )

    async def organizations(self):
        """
        show the organizations
        """

        def show():
            """ 
            """
            self.org_lod_grid = ListOfDictsGrid(lod=self.org_lod)
            pass

        await self.setup_content_div(show)

    async def persons(self):
        def show():
            
            self.person_lod_grid = ListOfDictsGrid(lod=self.person_lod)
            pass
        await self.setup_content_div(show)

    async def home(self, client: Client):
        def show():
            ui.label("CRM")

        await self.setup_content_div(show)
