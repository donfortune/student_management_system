import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget,  QTableWidgetItem
from PyQt6.QtGui import QAction
import sqlite3


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

        #create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no'))
        self.setCentralWidget((self.table)) #append the table to the main window



    def add_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)   #resets tables and avoids duplicates
        for row, data in enumerate(result):
            self.table.insertRow(row)
            for column, data_ in enumerate(data):
                self.table.setItem(row, column, QTableWidgetItem(str(data_)))
        connection.close()











app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.add_data()
sys.exit(app.exec())
