"""
Created on 2024-01-12

@author: wf
"""

import sys
from argparse import ArgumentParser

from ngwidgets.cmd import WebserverCmd

from crm.crm_web import CrmWebServer
from crm.fields import Fields
from crm.smartcrm_adapter import SmartCRMAdapter


class CrmCmd(WebserverCmd):
    """
    Command line for Customer Relationship Management
    """

    def getArgParser(self, description: str, version_msg) -> ArgumentParser:
        """
        override the default argparser call
        """
        parser = super().getArgParser(description, version_msg)
        parser.add_argument(
            "-rp",
            "--root_path",
            default=SmartCRMAdapter.root_path(),
            help="path to example dcm definition files [default: %(default)s]",
        )
        parser.add_argument(
            "--views",
            action="store_true",
            help="print the DDL of the English views generated from fields.yaml and exit",
        )
        parser.add_argument(
            "--view_db",
            default="smartcrm_en",
            help="database to hold the English views [default: %(default)s]",
        )
        parser.add_argument(
            "--source_db",
            default="smartcrm",
            help="database holding the legacy tables [default: %(default)s]",
        )
        return parser

    def handle_args(self, args) -> bool:
        """
        handle the command line arguments

        Args:
            args: the parsed arguments

        Returns:
            bool: True if the arguments were handled and the webserver is not to be started
        """
        handled = False
        if args.views:
            ddl = Fields.get().view_ddl(view_db=args.view_db, source_db=args.source_db)
            print(ddl)
            handled = True
        else:
            handled = super().handle_args(args)
        return handled


def main(argv: list = None):
    """
    main call
    """
    cmd = CrmCmd(
        config=CrmWebServer.get_config(),
        webserver_cls=CrmWebServer,
    )
    exit_code = cmd.cmd_main(argv)
    return exit_code


DEBUG = 0
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())
