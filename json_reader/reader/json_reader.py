import json
import traceback
import urllib.request
import uuid

from core.models import Node
from core.services.LoadDataService import LoadDataService


class JsonReader(LoadDataService):
    def name(self):
        return "JSON reader"

    def identifier(self):
        return "json_reader"

    def create_graph(self, file_path):
        try:
            if "http://" in file_path or "https://" in file_path or ".com" in file_path:
                response = urllib.request.urlopen(file_path)
                str_response = response.read().decode('utf-8')
                data = json.loads(str_response)
            else:
                with open(file_path, encoding="utf8") as data_file:
                    data = json.load(data_file)
        except Exception:
            traceback.print_exc()
            return [None]

        root_node = Node(str(uuid.uuid4()), "JSON Object", "Root")
        if isinstance(data, dict):
            for key in data.keys():
                self.create_graph_recursively(root_node, data[key], key)
        else:
            self.create_graph_recursively(root_node, data, "Unnamed")
        return [root_node]

    def create_graph_recursively(self, parent, data, name):
        if isinstance(data, dict):
            new_node = Node(str(uuid.uuid4()), "JSON Object", name)
            parent.neighbours.append(new_node)
            for key in data.keys():
                self.create_graph_recursively(new_node, data[key], key)

        elif isinstance(data, list):
            new_node = Node(str(uuid.uuid4()), "JSON Array", name)
            parent.neighbours.append(new_node)
            for item in data:
                self.create_graph_recursively(new_node, item, "Array element")

        elif isinstance(data, str):
            new_node = Node(str(uuid.uuid4()), "JSON String", name)
            new_node.attributes["value"] = data
            parent.neighbours.append(new_node)

        elif isinstance(data, (int, float)):
            new_node = Node(str(uuid.uuid4()), "JSON Number", name)
            new_node.attributes["value"] = data
            parent.neighbours.append(new_node)
