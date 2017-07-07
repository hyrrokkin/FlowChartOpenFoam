from pyqtgraph.Qt import QtGui, QtCore
from src.gui.MainWindow import *


app = QtGui.QApplication([])

main_window = MainWindow(700, 600)
main_window.show()


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
