import copy

from django.apps import apps
from django.shortcuts import render


def index(request):
    read_plugins = apps.get_app_config('core').read_plugins
    display_plugins = apps.get_app_config('core').display_plugins

    return render(request, "index.html",
                  {"title": "Index", "read_plugins": read_plugins, "display_plugins": display_plugins,
                   "data_loaded": data_loaded(request)})


def load_data(request):
    request.session["error"] = ""
    read_plugins = apps.get_app_config('core').read_plugins
    display_plugins = apps.get_app_config('core').display_plugins

    plugin_id = request.GET.get("plugin_id", None)
    file_path = request.GET.get("file_path", None)
    request.session["file_path"] = file_path
    print(file_path)

    plugin = read_plugins.get(plugin_id, None)
    if plugin is not None:
        plugin.load(request, file_path)

    if plugin is None or not data_loaded(request):
        request.session["error"] = "Error while loading data!"
        return render(request, "index.html",
                      {"title": "Index", "read_plugins": read_plugins, "display_plugins": display_plugins,
                       "data_loaded": data_loaded(request)})

    json_data = request.session["json_data"]

    return render(request, "tree_view.html",
                  {"title": "Index", "read_plugins": read_plugins, "display_plugins": display_plugins,
                   "json_data": json_data, "data_loaded": data_loaded(request)})


def display_data(request, plugin_id):
    request.session["display_plugin"] = plugin_id
    request.session["error"] = ""
    read_plugins = apps.get_app_config('core').read_plugins
    display_plugins = apps.get_app_config('core').display_plugins

    plugin = display_plugins.get(plugin_id, None)
    if plugin is None or not data_loaded(request):
        request.session["error"] = "Error while visualizing data!"
        return render(request, "index.html",
                      {"title": "Index", "read_plugins": read_plugins, "display_plugins": display_plugins,
                       "data_loaded": data_loaded(request)})

    mutable_graph_links = plugin.get_graph_links(request.session["mutable_graph"])
    persisted_graph_links = plugin.get_graph_links(request.session["persisted_graph"])
    graph_script = plugin.get_graph_script()
    json_data = request.session["json_data"]

    return render(request, "graph_view.html",
                  {"title": "Index", "read_plugins": read_plugins, "display_plugins": display_plugins,
                   "mutable_graph_links": mutable_graph_links, "persisted_graph_links": persisted_graph_links,
                   "graph_script": graph_script, "json_data": json_data, "data_loaded": data_loaded(request)})


def filter_data(request):
    plugin_id = request.session["display_plugin"]
    param = request.GET.get("filter_param", None)
    request.session["filter_param"] = param
    request.session["search_param"] = ""
    graph = request.session["persisted_graph"]

    result = []
    for node in graph:
        result = filter_data_recursively(param, [], node)

    request.session["mutable_graph"] = result

    return display_data(request, plugin_id)


def filter_data_recursively(param, result, node, parent=None):
    found = False
    if param.lower() in str(node.node_text).lower():
        found = True

    matching_node = copy.deepcopy(node)
    matching_node.neighbours = []

    if found:
        if parent is not None:
            parent.neighbours.append(matching_node)
        else:
            result.append(matching_node)

    for child in node.neighbours:
        if found:
            filter_data_recursively(param, result, child, matching_node)
        else:
            filter_data_recursively(param, result, child)
    return result


def search_data(request):
    plugin_id = request.session["display_plugin"]
    param = request.GET.get("search_param", None)
    request.session["search_param"] = param
    request.session["filter_param"] = ""

    graph = copy.deepcopy(request.session["persisted_graph"])
    for node in graph:
        search_data_recursively(param, node)
    request.session["mutable_graph"] = graph

    return display_data(request, plugin_id)


def search_data_recursively(param, node):
    node.selected = param.lower() in node.node_text.lower()
    for child in node.neighbours:
        search_data_recursively(param, child)


def data_loaded(request):
    return request.session.get("persisted_graph") is not None and request.session["persisted_graph"][0] is not None
