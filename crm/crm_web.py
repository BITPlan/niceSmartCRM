"""
Created on 2024-01-10

@author: wf
"""
from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from ngwidgets.webserver import WebserverConfig
from nicegui import Client, ui, run
from ngwidgets.lod_grid import ListOfDictsGrid, GridConfig

from crm.crm_core import CRM, Organizations, Persons
from crm.version import Version

class EntityIndex:
    def __init__(self):


class CrmSolution(InputWebSolution):
    """
    Customer Relationship Management solution
    """
    def __init__(self, webserver: "CrmWebServer", client: Client):
        super().__init__(webserver, client)
        self.organizations = Organizations()
        self.persons = Persons()
        self.org_lod = []
        self.person_lod = []
        self.org_lod_grid = None
        self.person_lod_grid = None

    def doUpdateEntities(self):
        """
        update entities
        """
        try:
            with self.header_row:
                self.org_count_label.set_text(f"Organizations: {len(self.org_lod)}")
                self.person_count_label.set_text(f"Persons: {len(self.person_lod)}")

            if self.org_lod_grid:
                self.org_lod_grid.load_lod(self.org_lod)
            if self.person_lod_grid:
                self.person_lod_grid.load_lod(self.person_lod)

        except Exception as ex:
            self.handle_exception(ex)

    async def updateEntities(self):
        await run.io_bound(self.doUpdateEntities)

    def setup_lod_grid(self, lod, key_col: str = "Id"):
        """
        setup the list of dicts grid
        """
        grid_config = GridConfig(
            key_col=key_col,
            editable=True,
            multiselect=True,
            with_buttons=False,
            debug=self.args.debug
        )
        lod_grid = ListOfDictsGrid(lod=lod, config=grid_config)
        lod_grid.set_checkbox_selection(key_col)
        return lod_grid

    def prepare_ui(self):
        pass

    async def home(self):
        """
        provide the main content page
        """
        def setup_home():
            with ui.row() as self.header_row:
                self.org_count_label = ui.label()
                self.person_count_label = ui.label()

            with ui.tabs() as tabs:
                ui.tab("Organizations")
                ui.tab("Persons")

            with ui.tab_panels(tabs, value="Organizations"):
                with ui.tab_panel("Organizations"):
                    self.org_lod_grid = self.setup_lod_grid(self.org_lod, key_col="Id")
                with ui.tab_panel("Persons"):
                    self.person_lod_grid = self.setup_lod_grid(self.person_lod, key_col="Id")

            ui.timer(0, self.updateEntities, once=True)

        await self.setup_content_div(setup_home)

class CrmWebServer(InputWebserver):
    """
    server for Customer Relationship Management
    """
    @classmethod
    def get_config(cls) -> WebserverConfig:
        copy_right = "(c)2024 Wolfgang Fahl"
        config = WebserverConfig(
            short_name="crm",
            copy_right=copy_right,
            version=Version(),
            default_port=9854
        )
        server_config = WebserverConfig.get(config)
        server_config.solution_class = CrmSolution
        return server_config

    def __init__(self):
        lods= {
            org:
        }
        self.org_lod = self.organizations.from_json_file()
            self.person_lod = self.persons.from_json_file()
        super().__init__(config=CrmWebServer.get_config())

