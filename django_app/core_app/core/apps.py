import pkg_resources
from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'core'
    read_plugins = {}
    display_plugins = {}

    def ready(self):
        self.read_plugins = load_plugins("data.read")
        self.display_plugins = load_plugins("data.display")


def load_plugins(ep_id):
    plugins = {}
    for ep in pkg_resources.iter_entry_points(group=ep_id):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins[ep.name] = plugin
    return plugins
