"""
Created on 2024-01-12

@author: wf
"""

import sys
from argparse import ArgumentParser

from ngwidgets.cmd import WebserverCmd

from crm.crm_web import CrmWebServer
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
        return parser


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
