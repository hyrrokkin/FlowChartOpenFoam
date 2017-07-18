from MainWindow import *
from Vertex import *
from src.core.Graph import *


"""
library = {
    'blockMesh': BlockMesh(),
    'icoFoam': Solver(),
    'paraFoam': ParaFoam()
}"""


def library(name):
    if name == 'blockMesh':
        return BlockMesh()

    if name == 'icoFoam':
        return Solver()

    if name == 'paraFoam':
        return ParaFoam()


class FlowChartView(QGraphicsView):
    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)

        self.__selected_vertex = None

    def graph(self):
        return self.parent().main_pane().graph()

    def run(self):
        self.__graph.run('/home/user/OpenFOAM/user-4.1/run/pitzDaily/')

    def add_vertex(self, text, x, y, width, height):
        vertex = VertexGui(width, height, text)
        vertex.setPos(x, y)

        self.scene().addItem(vertex)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.parent().library_tree().selectedIndexes():
                index = self.parent().library_tree().selectedIndexes()[0]
                text = index.model().itemFromIndex(index).text()
                self.add_vertex(text, event.x(), event.y(), 110, 65)
                self.graph().add_vertex(library(str(text)))
                self.parent().library_tree().clearSelection()
                return

        __items = self.scene().items(QPointF(event.x(), event.y()))
        selected_item = None

        if __items:
            for item in __items:
                if isinstance(item, VertexGui):
                    selected_item = item

        if True:
            if self.__selected_vertex:
                self.graph().connect(library(self.__selected_vertex.text()), library(selected_item.text()), Weight(1))
                print str(library(self.__selected_vertex.text())) + ' and ' + str(library(selected_item.text())) +\
                      ' connect'

                print self.__selected_vertex.scenePos()
                print selected_item.scenePos()

                line = QGraphicsLineItem(self.__selected_vertex.scenePos().x(), self.__selected_vertex.scenePos().y(), selected_item.scenePos().x(), selected_item.scenePos().y())

                line.setPen(QtGui.QPen(Qt.black, 5))

                self.scene().addItem(line)
                self.__selected_vertex = None
                return
            else:
                self.__selected_vertex = selected_item
                return

        #print self.graph

    def mouseMoveEvent(self, event):
        pass


class FlowChartScene(QGraphicsScene):
    def __init__(self, x, y, width, height, parent=None):
        QGraphicsScene.__init__(self, x, y, width, height, parent)


class FlowChart(QWidget):
    def __init__(self, main_pane=None):
        QWidget.__init__(self)

        self.__main_pane = main_pane

        self.__layout = QHBoxLayout(self)

        self.__scene = FlowChartScene(0.0, 0.0, self.useful_size()[0], self.useful_size()[1], self)
        self.__view = FlowChartView(self.__scene, self)

        self.__layout.addWidget(self.__view)

    def useful_size(self):
        return self.width() - (self.__layout.contentsMargins().left() + self.__layout.contentsMargins().right()), \
               self.height() - (self.__layout.contentsMargins().top() + self.__layout.contentsMargins().bottom())

    @property
    def main_pane(self):
        return self.__main_pane

    @property
    def library_tree(self):
        return self.parent().library_tree()

    def resize(self, width, height):
        super(FlowChart, self).resize(width, height)
        self.__scene.setSceneRect(0.0, 0.0, self.width(), self.height() + 22)

    def run(self):
        self.__view.run()

    def clear(self):
        self.__scene.clear()

