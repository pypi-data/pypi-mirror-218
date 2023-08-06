"""The Jupyter IAM Server application."""

import os

from traitlets import Unicode

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from .handlers import ConfigHandler, IndexHandler
from .echo.handler import WsEchoHandler
from .relay.handler import WsRelayHandler
from .proxy.handler import WsProxyHandler
from .pong.handler import WsPongHandler


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")


class DatalayerExampleExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Jupyter IAM Server extension."""

    name = "jupyter_iam"

    extension_url = "/jupyter_iam"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    config_a = Unicode("", config=True, help="Config A example.")
    config_b = Unicode("", config=True, help="Config B example.")
    config_c = Unicode("", config=True, help="Config C example.")

    def initialize_settings(self):
        self.log.info("Datalayer Config {}".format(self.config))

    def initialize_handlers(self):
        handlers = [
            ("jupyter_iam", IndexHandler),
            (url_path_join("jupyter_iam", "get_config"), ConfigHandler),
            (url_path_join("jupyter_iam", "echo"), WsEchoHandler),
            (url_path_join("jupyter_iam", "relay"), WsRelayHandler),
            (url_path_join("jupyter_iam", "proxy"), WsProxyHandler),
            (url_path_join("jupyter_iam", "pong"), WsPongHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = DatalayerExampleExtensionApp.launch_instance
