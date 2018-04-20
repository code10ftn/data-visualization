import os
from core.services.DisplayDataService import DisplayDataService
from pkg_resources import resource_string


class SimpleGraphVisualization(DisplayDataService):
    def __init__(self):
        self.links = []
        pass

    def name(self):
        return "Simple graph visualization"

    def identifier(self):
        return "simple_graph_visualization"

    def replace_special_characters(self, node):
        if len(str(node.node_text)) > 20: node.node_text = node.node_text[0:20] + "..."

        node.node_text = str(node.node_text).strip()
        node.node_id = node.node_id.replace('\\', '-')
        node.node_id = node.node_id.replace(";", "\;")
        node.node_id = node.node_id.replace(',', '\,')
        node.node_id = node.node_id.replace('"', '\\"')
        node.node_id = node.node_id.replace("'", "\\'")
        node.node_text = str(node.node_text).strip()
        node.node_text = " ".join(node.node_text.splitlines())

        node.node_text = str(node.node_text).replace('"', '``')
        node.node_text = str(node.node_text).replace("'", "`")

    def create_links(self, current_node, parent=None):
        self.replace_special_characters(current_node)

        if parent is None:
            self.links.append(
                "{ source: '" + current_node.node_id + "|" + current_node.node_text + "|" + str(current_node.selected) +
                "', target:'" + current_node.node_id + "|" + current_node.node_text + "|" + str(current_node.selected) + "' },")

        for node in current_node.neighbours:
            self.replace_special_characters(node)

            if "{ source: '" + current_node.node_id + "|" + current_node.node_text + "|" + str(current_node.selected) + \
                    "', target:'" + node.node_id + "|" + node.node_text + "|" + str(node.selected) + "' }," not in self.links:
                self.links.append(
                    "{ source: '" + current_node.node_id + "|" + current_node.node_text + "|" + str(current_node.selected) +
                    "', target:'" + node.node_id + "|" + node.node_text + "|" + str(node.selected) + "' },")
            self.create_links(node, current_node)
        return

    def get_graph_links(self, graph):
        self.links = []
        if not graph:
            return "[]"

        links = "["
        for g in graph:
            self.create_links(g)
        for l in self.links:
            links += l
        links = links[:-1] + "];"
        return links

    def get_graph_script(self):
        print(os.getcwd())
        return resource_string(__name__, 'simple_graph.js')

