import os
import sys
from Graph import *


def check_path(item):
    check_str(item)

    if not os.path.isdir(item):
        raise ValueError('item is not path')


class Project:
    def __init__(self, name='Untitled', path=os.path.expanduser('~/OFProject/'), graph=None, runFirst=0, clearPath=True):
        if "WM_PROJECT_VERSION" not in os.environ:
            print ('$WM_PROJECT_VERSION unset. FlowCart doesn not work that way') 
            sys.exit('Forcing quit.')    
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
        
        if clearPath:
            self.clean()
              
        if graph is None:
            self.__graph = Graph()
        else:
            check_graph(graph)
            self.__graph = graph

    @property
    def graph(self):
        return self.__graph

    def run(self, runFirst=0):
        try:
            self.__runFirst = int(runFirst)
        except ValueError:
            print "RunFirst parameter must be integer" 
        self.__graph.run(self.__path + self.__name, self.__runFirst)

    def clean(self):
        os.system('rm -rf ' + self.__path + self.__name + '/*')

    @property
    def path(self):
        return self.__path

    @property
    def case(self):
        return self.__path + '/case/'


def new_project(name='Untitled', path=os.path.expanduser('~/OFProject/')):
    return Project(name, path, Graph())

