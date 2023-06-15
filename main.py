import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):    #QMAINWINDOW ALLOWS FOR A MENU AND STATUS BAR
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        #creat menu bar
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')

        #create sub menu bar
        add_student = QAction('Add Student', self)
        file_menu.addAction(add_student)

        about_us = QAction('About', self)
        help_menu.addAction(about_us)
        about_us.setMenuRole(QAction.MenuRole.NoRole)   #add line if about doesnt show on the menu bar










app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
