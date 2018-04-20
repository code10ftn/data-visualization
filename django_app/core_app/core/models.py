class Node:
    def __init__(self, node_id=None, node_type="", node_text=""):
        self.node_id = node_id
        self.node_type = node_type
        self.node_text = node_text
        self.selected = False
        self.attributes = {}
        self.neighbours = []
