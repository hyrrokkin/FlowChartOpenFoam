import os
from Graph import *


def check_path(item):
    check_str(item)

    if not os.path.isdir(item):
        raise ValueError('item is not path')


class Project:
    def __init__(self, name='Untitled', path=os.path.expanduser('~/OFProject/'), graph=None):
        check_str(name)
        try:
            check_path(path)
        except ValueError:
            os.mkdir(path)
        try:
            check_path(path + name)
        except ValueError:
            os.mkdir(path + name)

        self.__name = name
        self.__path = path

        if graph is None:
            self.__graph = Graph()
        else:
            check_graph(graph)
            self.__graph = graph

    @property
    def graph(self):
        return self.__graph

    def run(self):
        self.__graph.run(self.__path + self.__name)
