import os
import platform
import time

from core.models import Node
from core.services.LoadDataService import LoadDataService

NODE_LIMIT = 2000


class FileSystemReader(LoadDataService):
    def __init__(self):
        self.root = None

    def name(self):
        return "File system reader"

    def identifier(self):
        return "file_system_reader"

    def create_graph(self, file_path):
        num = 0
        nodes = {}
        if file_path == "" or not os.path.isdir(file_path):
            return [None]

        for path, dirs, files in os.walk(file_path):
            if num > NODE_LIMIT:
                break
            num += 1
            if path in nodes:
                node = nodes[path]
            else:
                dir_name = os.path.basename(path)
                node = Node(path, "Directory", dir_name)

            self.set_dir_attributes(path, node)

            for file_name in files:
                num += 1
                full_path = os.path.join(path, file_name)
                new_node = Node(full_path, "File", file_name)
                node.neighbours.append(new_node)
                self.set_file_attributes(full_path, new_node)

            for dir_name in dirs:
                full_path = os.path.join(path, dir_name)
                new_node = Node(full_path, "Directory", dir_name)
                node.neighbours.append(new_node)
                nodes[full_path] = new_node

            if path == file_path:
                self.root = node

        return [self.root]

    def set_file_attributes(self, path, node):
        try:
            st = os.stat(path)
        except IOError:
            pass
        else:
            node.attributes["Size"] = st.st_size
            node.attributes["Time created"] = time.asctime(time.localtime(self.creation_date(path)))
            node.attributes["Time modified"] = time.asctime(time.localtime(st.st_mtime))

    def set_dir_attributes(self, path, node):
        try:
            st = os.stat(path)
        except IOError:
            pass
        else:
            node.attributes["Size"] = st.st_size
            node.attributes["Time created"] = time.asctime(time.localtime(self.creation_date(path)))
            node.attributes["Time modified"] = time.asctime(time.localtime(st.st_mtime))

    def creation_date(self, path_to_file):
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime
