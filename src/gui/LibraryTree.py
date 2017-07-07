from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.core.OFVertex import *


class OFItem(QStandardItem):
    def __init__(self, value):
        super(OFItem, self).__init__(str(value))

        self.__value = value
        self.setEditable(False)

    @property
    def value(self):
        return self.__value


class ReLibraryTree(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)

        self._indexes = {}
        self._size = 0

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.__treeView.customContextMenuRequested.connect(self.openMenu)
        self.setHeaderHidden(True)
        self.setModel(QStandardItemModel())
        self.add_items(self.model(), self.library())
        self.model().setHorizontalHeaderLabels([self.tr("Block")])

    def __call__(self, *args, **kwargs):
        return self

    def add_items(self, parent, elements):
        for e, children in elements:
            self._indexes[self._size] = e
            self._size += 1

            item = QStandardItem(e)

            parent.appendRow(item)
            if children:
                self.add_items(item, children)

    @staticmethod
    def library():
        return [
            ("Pre-processing", [
                ('blockMesh', [])
            ]),
            ("Solver", [
                ('icoFoam', [])
            ]),
            ("Post-processing", [
                ('paraFoam', [])
            ])
        ]


class LibraryTree(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self._indexes = {}
        self._size = 0

        self.__treeView = QTreeView()
        self.__treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__treeView.customContextMenuRequested.connect(self.openMenu)
        self.__treeView.setHeaderHidden(True)
        self.model = QStandardItemModel()
        self.add_items(self.model, self.library())
        self.__treeView.setModel(self.model)
        self.model.setHorizontalHeaderLabels([self.tr("Block")])
        layout = QVBoxLayout()
        layout.addWidget(self.__treeView)
        self.setLayout(layout)

    def selected(self):
        if self.__treeView.selectedIndexes():
            index = self.__treeView.selectedIndexes()[0]
            return index.model().itemFromIndex(index).text()
        else:
            return None

    def clear_select(self):
        self.tree_view.clearSelection()

    @property
    def tree_view(self):
        return self.treeView

    @staticmethod
    def library():
        return [
            ("Pre-processing", [
                (BlockMesh(), [])
            ]),
            ("Solver", [
                (Solver(), [])
            ]),
            ("Post-processing", [
                (ParaFoam, [])
            ])
        ]

    def add_items(self, parent, elements):
        for e, children in elements:
            self._indexes[self._size] = e
            self._size += 1

            if isinstance(e, str):
                item = QStandardItem(e)
            else:
                item = OFItem(e)

            parent.appendRow(item)
            if children:
                self.add_items(item, children)

    def openMenu(self, position):
        indexes = self.__treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        menu = QMenu()

        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.treeView.viewport().mapToGlobal(position))