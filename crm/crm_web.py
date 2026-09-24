"""
Created on 2024-01-10

@author: wf
"""

import os

import i18n
from basemkit.persistent_log import Log
from mogwai.core.mogwaigraph import MogwaiGraph, MogwaiGraphConfig
from mogwai.web.node_view import NodeTableView, NodeView, NodeViewConfig
from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from ngwidgets.webserver import WebserverConfig
from nicegui import Client, app, ui

from crm.crm_rest import CrmRestApi
from crm.db import DB
from crm.fields import Fields
from crm.i18n_config import I18nConfig
from crm.smartcrm_adapter import SmartCRMAdapter
from crm.version import Version


class CrmSolution(InputWebSolution):
    """
    Customer Relationship Management solution
    """

    def __init__(self, webserver: "CrmWebServer", client: Client):
        super().__init__(webserver, client)
        self.log = self.webserver.log
        self.graph = self.webserver.graph
        self.schema = self.webserver.schema

    def prepare_ui(self):
        pass

    def configure_menu(self):
        """
        configure additional non-standard menu entries
        """
        # Sorting the node types by display_order
        sorted_node_types = sorted(
            self.schema.node_type_configs.items(),
            key=lambda item: item[1].display_order,
        )

        for node_type_name, node_type in sorted_node_types:  # label e.g. project_list
            label_i18nkey = f"{node_type.label.lower()}_list"
            label = i18n.t(label_i18nkey)
            path = f"/nodes/{node_type_name}"
            self.link_button(label, path, node_type.icon, new_tab=False)

    async def show_nodes(self, node_type: str):
        """
        show nodes of the given type

        Args:
            node_type(str): the type of nodes to show
        """

        def show():
            try:
                config = NodeViewConfig(
                    solution=self,
                    graph=self.graph,
                    schema=self.schema,
                    node_type=node_type,
                )
                if not config.node_type_config:
                    ui.label(f"{i18n.t('invalid_node_type')}: {node_type}")
                    return
                node_table_view = NodeTableView(config=config)
                node_table_view.setup_ui()
            except Exception as ex:
                self.handle_exception(ex)

        await self.setup_content_div(show)

    async def show_node(self, node_type: str, node_id: str):
        """
        show the given node
        """

        def show():
            config = NodeViewConfig(
                solution=self, graph=self.graph, schema=self.schema, node_type=node_type
            )
            if not config.node_type_config:
                ui.label(f"{i18n.t('invalid_node_type')}: {node_type}")
                return
            # default view is the general NodeView
            view_class = NodeView
            # unless there is a specialization configured
            if config.node_type_config._viewclass:
                view_class = config.node_type_config._viewclass
            node_view = view_class(config=config, node_id=node_id)
            node_view.setup_ui()
            pass

        await self.setup_content_div(show)


class CrmWebServer(InputWebserver):
    """
    server for Customer Relationship Management
    """

    @classmethod
    def get_config(cls) -> WebserverConfig:
        copy_right = "(c)2024-2025 Wolfgang Fahl"
        config = WebserverConfig(
            short_name="crm",
            copy_right=copy_right,
            version=Version(),
            default_port=9854,
        )
        server_config = WebserverConfig.get(config)
        server_config.solution_class = CrmSolution
        return server_config

    def __init__(self):
        super().__init__(config=CrmWebServer.get_config())
        self.log = Log()
        config = MogwaiGraphConfig(name_field="_node_name", index_config="minimal")
        self.graph = MogwaiGraph(config=config)

        @ui.page("/nodes/{node_type}")
        async def show_nodes(client: Client, node_type: str):
            """
            show the nodes of the given type
            """
            await self.page(client, CrmSolution.show_nodes, node_type)

        @ui.page("/node/{node_type}/{node_id}")
        async def node(client: Client, node_type: str, node_id: str):
            """
            show the node with the given node_id
            """
            await self.page(client, CrmSolution.show_node, node_type, node_id)

    def configure_run(self):
        """
        configure with args
        """
        # args = self.args
        I18nConfig.config()

        InputWebserver.configure_run(self)
        # the graph schema comes from fields.yaml like the field mapping and the labels
        self.schema = Fields.get().graph_schema()
        self.schema.add_to_graph(self.graph)
        try:
            self.db = DB()
        except Exception as ex:
            self.log.log(
                "⚠️", "db", f"database not available - falling back to JSON: {ex}"
            )
            self.db = None

        topics = SmartCRMAdapter.get_topics()
        for topic in topics:
            adapter = SmartCRMAdapter(topic=topic)
            if self.db is not None:
                lod = adapter.from_db(self.db)
            else:
                lod = adapter.from_json_file()
            for index, record in enumerate(lod):
                _node = self.graph.add_labeled_node(
                    topic.name, name=f"{topic.name}-{index}", properties=record
                )
            print(f"loaded {len(lod)} {topic.name} records")
        # read-only REST API mounted into NiceGUI's FastAPI app
        self.rest_api = CrmRestApi(db=self.db)
        app.include_router(self.rest_api.router)
