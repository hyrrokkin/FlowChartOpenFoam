from MainWindow import *
from Vertex import *
from src.core.Graph import *


"""
library = {
    'blockMesh': BlockMesh(),
    'solver': Solver(),
    'paraFoam': ParaFoam()
}"""


def show_dialog(text, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Error")
    msg.setInformativeText(text)
    msg.setWindowTitle("Error!")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print "value of pressed message box button:", retval


def msgbtn(i):
    print "Button pressed is:", i.text()


def library(name, project):
    if name == 'blockMesh':
        return BlockMesh(ofDictPath=project.path + '/case/system/blockMeshDict')

    if name == 'solver':
        return Solver(tutorialPath=project.path + '/case')

    if name == 'paraFoam':
        return ParaFoam()


class FlowChartView(QGraphicsView):
    def __init__(self, scene, parent=None):
        QGraphicsView.__init__(self, scene, parent)

        self.__selected_vertex = None

    def graph(self):
        return self.parent().main_pane().graph()

    @property
    def project(self):
        return self.parent().main_pane().project

    def run(self):
        self.graph().run(self.project.case)

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
                self.graph().add_vertex(library(str(text), self.parent().main_pane.project))
                self.parent().library_tree().clearSelection()
                print self.graph()
                return

        __items = self.scene().items(QPointF(event.x(), event.y()))
        selected_item = None

        if __items:
            for item in __items:
                if isinstance(item, VertexGui):
                    selected_item = item

        if event.modifiers() == Qt.AltModifier:
            print self.graph()
            if self.__selected_vertex:
                """if not self.graph().connect(library(self.__selected_vertex.text(), self.parent().main_pane.project),
                                     library(selected_item.text(), self.parent().main_pane.project), Weight(1)):"""
                if not self.graph().connect(self.graph().find_vertex(self.__selected_vertex.text()),
                                            self.graph().find_vertex(selected_item.text()), Weight(1)):
                    show_dialog('Connect error!', self)
                    print 'connect error!'
                else:
                    if self.__selected_vertex.pos().x() + self.__selected_vertex.rect().width() < selected_item.pos().x():
                        self.connect_line(self.__selected_vertex, selected_item)
                    elif self.__selected_vertex.pos().x() + self.__selected_vertex.rect().width() > selected_item.pos().x():
                        self.connect_line(selected_item, self.__selected_vertex)

                    print str(self.graph().find_vertex(self.__selected_vertex.text())) + ' and ' + str(
                        self.graph().find_vertex(selected_item.text())) + \
                          ' connect'

                    self.__selected_vertex = None

                    return
            else:
                self.__selected_vertex = selected_item
                return
        else:
            self.__selected_vertex = None
        """if True:
            if self.__selected_vertex:
                self.graph().connect(library(self.__selected_vertex.text(), self.parent().main_pane.project), library(selected_item.text(), self.parent().main_pane.project), Weight(1))
                print str(library(self.__selected_vertex.text(), self.parent().main_pane.project)) + ' and ' + str(library(selected_item.text(), self.parent().main_pane.project)) +\
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
                return"""

        #print self.graph

    def mouseMoveEvent(self, event):
        pass

    def connect_line(self, from_item, to_item):
        if from_item.pos().y() + from_item.rect().height() < to_item.pos().y():
            line = QGraphicsLineItem(
                from_item.scenePos().x() + from_item.rect().width(),
                from_item.scenePos().y() + from_item.rect().height() / 2,
                to_item.scenePos().x() + to_item.rect().width() / 2,
                to_item.scenePos().y())
        elif from_item.pos().y() > to_item.pos().y() + to_item.rect().height():
            line = QGraphicsLineItem(
                from_item.scenePos().x() + from_item.rect().width(),
                from_item.scenePos().y() + from_item.rect().height() / 2,
                to_item.scenePos().x() + to_item.rect().width() / 2,
                to_item.scenePos().y() + to_item.rect().height())
        else:
            line = QGraphicsLineItem(
                from_item.scenePos().x() + from_item.rect().width(),
                from_item.scenePos().y() + from_item.rect().height() / 2,
                to_item.scenePos().x(),
                to_item.scenePos().y() + to_item.rect().height() / 2)

        line.setPen(QtGui.QPen(Qt.black, 5))

        self.scene().addItem(line)


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

