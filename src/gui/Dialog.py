from MainWindow import *
import os

from src.core.Project import new_project

dir_path = '/opt/OpenFOAM/OpenFOAM-4.1/tutorials/'


def subdir(dir_name):
    sub_dict = dict()
    names = os.listdir(dir_name)
    for name in names:
        fullname = os.path.join(dir_name, name)
        if os.path.isdir(fullname):
            sub_dict[name] = fullname
    return sub_dict


class NewProjectDialog(QDialog):
    def __init__(self, width, height, parent=None):
        super(NewProjectDialog, self).__init__(parent)

        self.resize(width, height)

        self.path_label = self.create_path_label()
        self.path_line_edit = self.create_path_line_edit()

        self.empty_project = self.create_empty_radio_button()
        self.tutorial_project = self.create_tutorial_radio_button()

        self.__tutorials = self.tutorials_tree()

        self.create_button = self.create_create_button()
        self.close_button = self.create_close_button()

        l = QVBoxLayout(self)

        l.addWidget(self.path_label)
        l.addWidget(self.path_line_edit)

        l.addWidget(self.empty_project)
        l.addWidget(self.tutorial_project)

        l.addWidget(self.create_button)
        l.addWidget(self.close_button)

        l.addItem(self.create_project_path_line())
        l.addItem(self.create_check_box_line())
        l.addWidget(self.__tutorials)
        l.addItem(self.create_buttons_line())

    def create_empty_radio_button(self):
        radio_button = QRadioButton('Empty')
        radio_button.setChecked(True)
        radio_button.clicked.connect(self.hide_tree)
        return radio_button

    def create_tutorial_radio_button(self):
        radio_button = QRadioButton('From tutorials')
        radio_button.clicked.connect(self.show_tree)
        return radio_button

    def show_tree(self):
        if not self.__tutorials.isVisible():
            self.__tutorials.setVisible(True)
            self.resize(self.width(), self.height() + 150)

    def hide_tree(self):
        if self.__tutorials.isVisible():
            self.__tutorials.setVisible(False)
            self.resize(self.width(), self.height() - 150)

    @staticmethod
    def create_path_label():
        label = QLabel('Location:')
        return label

    @staticmethod
    def create_path_line_edit():
        line_edit = QLineEdit()
        line_edit.setText(os.getenv("HOME") + '/OFProject/')
        return line_edit

    def create_project_path_line(self):
        layout = QHBoxLayout()
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_line_edit)
        layout.setSpacing(10)

        return layout

    def create_check_box_line(self):
        layout = QHBoxLayout()
        layout.addWidget(self.empty_project)
        layout.addWidget(self.tutorial_project)
        layout.setSpacing(10)

        return layout

    def create_create_button(self):
        create_button = QPushButton('Create', self)
        create_button.clicked.connect(self.create_button_action)
        return create_button

    def create_close_button(self):
        close_button = QPushButton('Close', self)
        close_button.clicked.connect(self.close_button_action)
        return close_button

    def create_buttons_line(self):
        layout = QHBoxLayout()
        layout.addWidget(self.create_button)
        layout.addWidget(self.close_button)
        layout.setSpacing(10)

        return layout

    def create_button_action(self):
        if self.empty_project.isChecked():
            os.mkdir(self.path_line_edit.text())
        if self.tutorial_project.isChecked() and self.__tutorials.selectedIndexes():
            index = self.__tutorials.selectedIndexes()[0]
            selected_item = index.model().itemFromIndex(index)
            path = dir_path + \
                   selected_item.parent().parent().text() + '/' + \
                   selected_item.parent().text() + '/' + \
                   selected_item.text() + '/'

            os.mkdir(self.path_line_edit.text())
            os.mkdir(self.path_line_edit.text() + '/case')
            os.system('cp -R ' + str(path) + '* ' + str(self.path_line_edit.text() + '/case'))

            print path

        tmp = str(self.path_line_edit.text()).split('/')
        project = new_project(name=tmp[len(tmp) - 1], path=str(self.path_line_edit.text()))
        self.parent().new_project(project)

        self.close()

    def close_button_action(self):
        self.close()

    def tutorials_tree(self):
        tree = QTreeView()

        tree.setHeaderHidden(True)
        tree.setModel(QStandardItemModel())
        tree.model().setHorizontalHeaderLabels([tree.tr("Tutorials")])
        tree.setVisible(False)

        first = subdir(dir_path)

        for first_key in first:
            first_item = QStandardItem(first_key)
            first_item.setSelectable(False)
            tree.model().appendRow(first_item)

            second = subdir(first[first_key])

            for second_key in second:
                second_item = QStandardItem(second_key)
                second_item.setSelectable(False)
                first_item.appendRow(second_item)

                third = subdir(second[second_key])

                for third_key in third:
                    third_item = QStandardItem(third_key)
                    third_item.setSelectable(True)
                    second_item.appendRow(third_item)
        return tree
