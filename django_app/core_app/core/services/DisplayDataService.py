import abc


class DisplayDataService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def identifier(self):
        pass

    @abc.abstractmethod
    def get_graph_links(self, graph):
        pass

    @abc.abstractmethod
    def get_graph_script(self):
        pass
