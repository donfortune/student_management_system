import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, QTableWidget,  QTableWidgetItem, QDialog
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
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)

        about_us = QAction('About', self)
        help_menu.addAction(about_us)
        about_us.setMenuRole(QAction.MenuRole.NoRole)   #add line if about doesnt show on the menu bar

        #create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no'))
        self.setCentralWidget((self.table)) #append the table to the main window
        self.table.verticalHeader().setVisible(False) #removed duplicate index



    def add_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)   #resets tables and avoids duplicates
        for row, data in enumerate(result):
            self.table.insertRow(row)
            for column, data_ in enumerate(data):
                self.table.setItem(row, column, QTableWidgetItem(str(data_)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText('Name')
        layout.addWidget(self.name)

        self.courses = QComboBox()
        self.courses.addItems(['Biology', 'Maths', 'Chemistry', 'Physics'])
        layout.addWidget(self.courses)

        self.phone_name = QLineEdit()
        self.phone_name.setPlaceholderText('Phone No.')
        layout.addWidget(self.phone_name)

        button = QPushButton('Submit')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
        name = self.name.text()
        course = self.courses.itemText(self.courses.currentIndex())
        mobile = self.phone_name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', (name, course, mobile))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.add_data()














app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.add_data()
sys.exit(app.exec())
