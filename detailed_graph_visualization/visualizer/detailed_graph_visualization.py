from core.models import Node
from core.services.DisplayDataService import DisplayDataService
import math
from pkg_resources import resource_string


class DetailedGraphVisualization(DisplayDataService):
    def __init__(self):
        self.links = []
        self.found = []
        self.row_chars = 30
        self.graph = Node()

    def name(self):
        return "Detailed graph visualization"

    def identifier(self):
        return "detailed_graph_visualization"

    def format_node(self, node):
        node.node_id = node.node_id.replace('\\', '-')
        node.node_id = node.node_id.replace(";", "\;")
        node.node_id = node.node_id.replace(',', '\,')
        node.node_id = node.node_id.replace('"', '\\"')
        node.node_id = node.node_id.replace("'", "\\'")

        if node.node_text is None:
            return

        node.node_text = str(node.node_text).replace('"', '`')
        node.node_text = str(node.node_text).replace("'", "`")
        node.node_text = str(node.node_text).strip()
        node.node_text = " ".join(node.node_text.splitlines())

        if len(node.node_text) > self.row_chars and '+' not in node.node_text:
            parts = math.ceil(len(node.node_text) / self.row_chars)
            text = node.node_text
            node.node_text = ""
            for i in range(1, parts):
                node.node_text += text[(i - 1) * self.row_chars:i * self.row_chars] + '+'
            node.node_text += text[(parts - 1) * self.row_chars:]

    def format_attributes(self, node):
        attr = ""
        attr += "+" + "Type : " + str(node.node_type)
        for a in node.attributes:
            if node.attributes[a] is None:
                continue

            curr_att = a + ":" + str(node.attributes[a])

            curr_att = curr_att.replace('\\', '-')
            curr_att = curr_att.replace(";", "\;")
            curr_att = curr_att.replace(',', '\,')
            curr_att = curr_att.replace('"', '`')
            curr_att = curr_att.replace("'", "`")
            curr_att = curr_att.strip()
            curr_att = " ".join(curr_att.splitlines())

            if len(curr_att) > self.row_chars:
                parts = math.ceil(len(curr_att) / self.row_chars)
                text = curr_att
                curr_att = ""
                for i in range(1, parts):
                    curr_att += text[(i - 1) * self.row_chars:i * self.row_chars] + '+'
                curr_att += text[(parts - 1) * self.row_chars:]
            attr += "+" + curr_att

        return attr

    def create_links(self, graph, parent=None):
        self.format_node(graph)
        gattr = self.format_attributes(graph)

        if parent is None:
            self.links.append(
                "{ source: '" + graph.node_id + "|" + graph.node_text + " " + gattr + "|" +
                str(graph.selected) + "', target:'" + graph.node_id + "|" + graph.node_text + " " +
                gattr + "|" + str(graph.selected) + "' },")

        for node in graph.neighbours:
            self.format_node(node)
            attr = self.format_attributes(node)

            if "{ source: '" + graph.node_id + "|" + graph.node_text + " " + gattr + "|" + str(graph.selected) + \
                    "', target:'" + node.node_id + "|" + node.node_text + " " + attr + "|" + str(node.selected) + \
                    "' }," not in self.links:
                self.links.append(
                    "{ source: '" + graph.node_id + "|" + graph.node_text + " " + gattr + "|" +
                    str(graph.selected) + "', target:'" + node.node_id + "|" + node.node_text +
                    " " + attr + "|" + str(node.selected) + "' },")
            self.create_links(node, graph)

        return

    def get_graph_links(self, graph):

        if not graph:
            return "[]"

        links = ""
        self.links = []
        self.links.append("[")

        for g in graph:
            self.create_links(g)

        for l in self.links:
            links += l
        links = links[:-1] + "];"

        return links

    def get_graph_script(self):
        return resource_string(__name__, 'detailed_graph.js')
