import abc
import json


class LoadDataService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    def load(self, request, file_path):
        graph = self.create_graph(file_path)
        request.session["mutable_graph"] = graph  # used for search and filter
        request.session["persisted_graph"] = graph  # used for tree and bird view
        request.session["json_data"] = self.graph_to_json(request)

    @abc.abstractmethod
    def create_graph(self, file_path):
        pass

    def graph_to_json(self, request):
        graph = request.session["persisted_graph"]
        if graph is None or graph[0] is None:
            return json.dumps({}, ensure_ascii=False)
        if len(graph) > 1:
            json_data = {"name": "root", "children": []}
            for node in graph:
                if node is not None:
                    self.graph_to_json_recursively(node, json_data["children"])
            return json.dumps(json_data, ensure_ascii=False)
        else:
            json_data = {"name": graph[0].node_text}
            if graph[0].neighbours:
                json_data["children"] = []
                for child in graph[0].neighbours:
                    self.graph_to_json_recursively(child, json_data["children"])
            return json.dumps(json_data, ensure_ascii=False)

    def graph_to_json_recursively(self, node, parent_list):
        new_node = {"name": node.node_text}
        if node.neighbours:
            new_node["children"] = []
            for child in node.neighbours:
                self.graph_to_json_recursively(child, new_node["children"])
        parent_list.append(new_node)
