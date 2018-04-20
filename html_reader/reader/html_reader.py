import traceback
import urllib.request
import uuid
from html.parser import HTMLParser

from core.models import Node
from core.services.LoadDataService import LoadDataService


class HtmlReader(LoadDataService, HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.void_elements = {"area", "base", "br", "col", "embed", "hr", "img", "input",
                              "keygen", "link", "meta", "param", "source", "track", "wbr"}
        self.root = None
        self.current = None
        self.stack = []

    def name(self):
        return "HTML reader"

    def identifier(self):
        return "html_reader"

    def create_graph(self, file_path):
        self.root = None
        self.stack = []
        try:
            if "http://" in file_path or "https://" in file_path or ".com" in file_path:
                with urllib.request.urlopen(file_path) as url:
                    self.feed(str(url.read()))
            else:
                with open(file_path, encoding="utf8") as data_file:
                    self.feed(data_file.read())
        except Exception:
            traceback.print_exc()
            return [None]

        return [self.root]

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if self.root is None:
            self.root = Node(str(uuid.uuid4()), "tag", tag)
            self.current = self.root
            for attr in attrs:
                self.current.attributes[attr[0]] = attr[1]
            self.stack.append(self.current)
        else:
            new_node = Node(str(uuid.uuid4()), "tag", tag)
            for attr in attrs:
                new_node.attributes[attr[0]] = attr[1]
            self.current.neighbours.append(new_node)
            if tag not in self.void_elements:
                self.current = new_node
                self.stack.append(self.current)

    def handle_endtag(self, tag):
        if self.stack and self.stack[len(self.stack) - 1].node_text == tag:
            self.stack.pop()
            if self.stack:
                self.current = self.stack[len(self.stack) - 1]
        elif tag not in self.void_elements:
            print("Not a good html format!")

    def handle_startendtag(self, tag, attrs):
        new_node = Node(str(uuid.uuid4()), "tag", tag)
        for attr in attrs:
            new_node.attributes[attr[0]] = attr[1]
        self.current.neighbours.append(new_node)

    def handle_data(self, data):
        if self.current is not None:
            data = data.replace("\\n", "")
            data = data.strip()
            if not data.isspace() and data != "":
                text_node = Node(str(uuid.uuid4()), "text", "text")
                text_node.attributes["content"] = data
                self.current.neighbours.append(text_node)
