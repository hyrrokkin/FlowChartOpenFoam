from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class EdgeSquare(QGraphicsRectItem):
    def __init__(self, width, height, _parent=None):
        super(QGraphicsRectItem, self).__init__(_parent)

        self.setPen(QtGui.QPen(Qt.blue, 0))
        self.setBrush(QBrush(Qt.blue))
        self.setFlag(self.ItemSendsScenePositionChanges, True)

        self.setRect(0, 0, width, height)


class VertexText(QGraphicsTextItem):
    def __init__(self, text, parent):
        super(QGraphicsTextItem, self).__init__(text)

        self.__text = text

        self.setParentItem(parent)
        self.setDefaultTextColor(QColor(QtCore.Qt.black))

    def text(self):
        return self.__text


class VertexGui(QGraphicsRectItem):
    def __init__(self, width, height, text="Untitled"):
        super(VertexGui, self).__init__()

        self.__text = VertexText(text, self)

        self.setPen(QtGui.QPen(Qt.black, 5))
        self.setBrush(QtGui.QBrush(Qt.lightGray))
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable | self.ItemIsFocusable)

        self.setRect(0, 0, width, height)

    def text(self):
        return str(self.__text.text())

    def center_text(self, width, height):
        rect = self.__text.boundingRect()
        lw, lh = rect.width(), rect.height()
        lx = (width - lw) / 2
        ly = (height - lh) / 2
        self.__text.setPos(lx, ly)

    def setRect(self, x, y, width, height):
        super(VertexGui, self).setRect(x, y, width, height)

        self.center_text(width, height)
