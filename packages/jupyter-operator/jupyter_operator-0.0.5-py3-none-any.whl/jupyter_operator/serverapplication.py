"""The Jupyter Operator Server application."""

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


class JupyterOperatorExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Jupyter Operator Server extension."""

    name = "jupyter_operator"

    extension_url = "/jupyter_operator"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]
    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]

    config_a = Unicode("", config=True, help="Config A example.")
    config_b = Unicode("", config=True, help="Config B example.")
    config_c = Unicode("", config=True, help="Config C example.")

    def initialize_settings(self):
        self.log.info("Jupyter Operator Config {}".format(self.config))

    def initialize_handlers(self):
        base_url = self.serverapp.web_app.settings["base_url"]
        handlers = [
            (url_path_join(base_url, "jupyter_operator"), IndexHandler),
            (url_path_join(base_url, "jupyter_operator", "get_config"), ConfigHandler),
            (url_path_join(base_url, "jupyter_operator", "echo"), WsEchoHandler),
            (url_path_join(base_url, "jupyter_operator", "relay"), WsRelayHandler),
            (url_path_join(base_url, "jupyter_operator", "proxy"), WsProxyHandler),
            (url_path_join(base_url, "jupyter_operator", "pong"), WsPongHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = JupyterOperatorExtensionApp.launch_instance
