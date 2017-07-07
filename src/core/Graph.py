from abc import ABCMeta, abstractmethod
from numbers import Number


def is_none(item):
    return item is None


def is_number(item):
    return isinstance(item, Number)


def is_str(item):
    return isinstance(item, str)


def is_weight(item):
    return isinstance(item, Weight)


def is_vertex(item):
    return isinstance(item, Vertex)


def is_graph(item):
    return isinstance(item, Graph)


def check_none(item):
    if is_none(item):
        raise ValueError("item can't be None ")


def check_number(item):
    check_none(item)
    if not is_number(item):
        raise TypeError("item isn't instance Number")


def check_str(item):
    check_none(item)
    if not is_str(item):
        raise TypeError("item isn't instance String")


def check_weight(item):
    check_none(item)
    if not is_weight(item):
        raise TypeError("item isn't instance Weight")


def check_vertex(item):
    check_none(item)
    if not is_vertex(item):
        raise TypeError("item isn't instance Vertex")


def check_graph(item):
    check_none(item)
    if not is_graph(item):
        raise TypeError("item isn't instance Graph")


class Weight:
    def __init__(self, value):
        check_none(value)
        self.__value = value

    def __hash__(self):
        return hash(self.__value)

    def __str__(self):
        return 'Weight [' + self.__value + ']'

    def __eq__(self, other):
        check_weight(other)
        return self.__value == other.__value

    def __ne__(self, other):
        check_weight(other)
        return not self == other

    def __lt__(self, other):
        check_weight(other)
        return self.__value < other.__value

    def __le__(self, other):
        check_weight(other)
        return self == other or self < other

    def __gt__(self, other):
        check_weight(other)
        return self.__value > other.__value

    def __ge__(self, other):
        check_weight(other)
        return self == other or self > other


class Vertex:
    __metaclass__ = ABCMeta

    def __init__(self, identify=-1, name='Untitled'):
        check_number(identify)
        check_str(name)

        self.__id = identify
        self.__name = name
        self.__adjacency_list = {}

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @id.setter
    def id(self, identify):
        check_number(identify)
        self.__id = identify

    @name.setter
    def name(self, name):
        check_str(name)
        self.__name = name

    def __hash__(self):
        return hash(self.__id) + hash(self.__name)

    def __str__(self):
        return '[Vertex: name=' + self.name + ']'

    def __eq__(self, other):
        check_vertex(other)
        return self.name == other.name

    def __ne__(self, other):
        check_vertex(other)
        return not self == other

    def is_connected(self, vertex):
        check_vertex(vertex)
        return vertex in self.__adjacency_list

    def weight_connection(self, vertex):
        check_vertex(vertex)
        if self.is_connected(vertex):
            return self.__adjacency_list[vertex]
        return None

    def update_weight_connection(self, vertex, weight):
        check_vertex(vertex)
        check_weight(weight)
        if self.is_connected(vertex):
            self.__adjacency_list[vertex] = weight
            return True
        return False

    def connect(self, vertex, weight):
        check_vertex(vertex)
        check_weight(weight)
        if self.is_connected(vertex):
            return False
        self.__adjacency_list[vertex] = weight
        return True

    def disconnect(self, vertex):
        check_vertex(vertex)
        if self.is_connected(vertex):
            del self.__adjacency_list[vertex]
            return True
        return False

    def clear_connections(self):
        self.__adjacency_list.clear()

    def edges(self):
        return self.__adjacency_list

    @abstractmethod
    def action(self, **kwargs):
        pass


class Graph:
    def __init__(self):
        self.__vertices = []

    def __contains__(self, item):
        check_vertex(item)
        return item in self.__vertices

    def run(self, path):
        if len(self.__vertices) > 0:
            self.__vertices[0].action(path=path)

    def get_vertex(self, identify):
        check_number(identify)

        if identify < len(self.__vertices):
            return self.__vertices[identify]

        raise IndexError('id >= len(self.__vertices)')

    def find_vertex(self, name):
        check_str(name)

        for vertex in self.__vertices:
            if vertex.name == name:
                return vertex

        return None

    def add_vertex(self, vertex):
        check_vertex(vertex)
        if vertex in self:
            return False
        vertex.id = len(self.__vertices)
        vertex.clear_connections()
        self.__vertices.append(vertex)
        return True

    def remove_vertex(self, vertex):
        check_vertex(vertex)
        if vertex not in self:
            return False

        for aVertex in self.__vertices:
            aVertex.disconnect(vertex)

        self.__vertices.remove(vertex)

        for i in range(vertex.id, len(self.__vertices)):
            self.__vertices[i].id = i

        return True

    def connect(self, from_vertex, to_vertex, weight):
        check_vertex(from_vertex)
        check_vertex(to_vertex)
        check_weight(weight)

        if from_vertex == to_vertex:
            return False

        if from_vertex not in self or to_vertex not in self:
            return False

        self.__vertices[from_vertex.id].connect(to_vertex, weight)

    def disconnect(self, from_vertex, to_vertex):
        check_vertex(from_vertex)
        check_vertex(to_vertex)

        if from_vertex not in self or to_vertex not in self:
            return False

        return self.__vertices[from_vertex.id].disconnect(to_vertex)

    def __str__(self):
        output = 'Graph [ '

        for vertex in self.__vertices:
            output += str(vertex.id) + ':' + str(vertex) + ', '

        output = output[:len(output) - 2] + ' ]'

        return output
