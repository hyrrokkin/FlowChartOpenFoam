from LibraryTree import *
from FlowChart import FlowChart
from PyQt4.QtCore import *
from Dialog import *
from src.core.Project import Project


class Editor(QWidget):
    def __init__(self, main_pane=None):
        super(Editor, self).__init__()

        self.__main_pane = main_pane

        self.__library_tree = ReLibraryTree()
        self.__flow_chart = FlowChart(main_pane=main_pane)

        self.setLayout(self.__create_layout(self.__library_tree, self.__flow_chart))

    def __call__(self, *args, **kwargs):
        return self

    @property
    def main_pane(self):
        return self.__main_pane

    @property
    def library_tree(self):
        return self.__library_tree

    @property
    def flow_chart(self):
        return self.__flow_chart

    @staticmethod
    def __create_layout(*items):
        vbox = QHBoxLayout()

        vbox.setSpacing(10)
        vbox.setContentsMargins(10, 10, 10, 10)

        for item in items:
            vbox.addWidget(item)

        return vbox

    def selected(self):
        return self.__library_tree.selected()

    def clear_select(self):
        return self.__library_tree.clear_select()

    def decorated_size(self):
        return self.layout().contentsMargins().left() + self.layout().contentsMargins().right() + \
               self.layout().spacing(), \
               self.layout().contentsMargins().top() + self.layout().contentsMargins().bottom()

    def content_size(self):
        return self.width() - self.decorated_size()[0], self.height() - self.decorated_size()[1]

    def resize(self, width, height):
        super(Editor, self).resize(width, height)

        print self.content_size()

        self.__library_tree.resize(self.content_size()[0] * 0.3, self.content_size()[1])
        self.__flow_chart.resize(self.content_size()[0] * 0.6, self.content_size()[1])

    def run(self):
        self.__flow_chart.run()


class MainWindow(QMainWindow):
    def __init__(self, width, height, project=Project()):
        super(MainWindow, self).__init__()
        self.__project = project

        self.setWindowTitle('OpenFOAM FlowChart')

        self.__menu_bar = self.__create_menu_bar()
        self.__editor = Editor(main_pane=self)

        self.setCentralWidget(self.__editor)

        self.resize(width, height)

    def __call__(self, *args, **kwargs):
        return self

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, project):
        self.__project = project

    @property
    def graph(self):
        return self.__project.graph

    def run(self):
        self.__editor.run()

    def new_project_dialog_show(self):
        pd = NewProjectDialog(300, 150, self)
        pd.exec_()

    def __create_menu_bar(self):
        def create_file_menu():
            new_item = QAction('New', self)
            save_item = QAction('Save', self)
            load_item = QAction('Load', self)
            exit_item = QAction('Exit', self)

            file_menu = menu_bar.addMenu('&File')

            file_menu.addAction(new_item)
            file_menu.addAction(save_item)
            file_menu.addAction(load_item)
            file_menu.addAction(exit_item)

            self.connect(new_item, SIGNAL('triggered()'), self.new_project_dialog_show)

        def create_run_menu():
            run_item = QAction('Run', self)
            #run_item.triggered().connect(self.run)

            run_menu = menu_bar.addMenu('&Run')

            self.connect(run_item, SIGNAL('triggered()'), self.run)

            run_menu.addAction(run_item)

        def create_help_menu():
            help_menu = menu_bar.addMenu('&Help')

            about_item = QAction('About', self)

            help_menu.addAction(about_item)

        menu_bar = self.menuBar()

        create_file_menu()
        create_run_menu()
        create_help_menu()

        return menu_bar

    @property
    def library_tree(self):
        return self.parent().library_tree()

    def resize(self, width, height):
        super(MainWindow, self).resize(width, height)

        self.__editor.resize(width - 23, height - self.__menu_bar.height() - 44)

    def new_project(self, project):
        self.__editor.flow_chart.clear()
        self.__project = project



