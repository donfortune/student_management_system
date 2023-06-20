import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QStatusBar,  QGridLayout, QLineEdit,  QPushButton, QComboBox, QMainWindow, QTableWidget,  QTableWidgetItem, QDialog, QToolBar
from PyQt6.QtGui import QAction,  QIcon
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):    #QMAINWINDOW ALLOWS FOR A MENU AND STATUS BAR
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)
        #creat menu bar
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        search_menu = self.menuBar().addMenu('&Edit')

        #create sub menu bar
        add_student = QAction(QIcon('icons/add.png'),'Add Student', self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)

        about_us = QAction('About', self)
        help_menu.addAction(about_us)
        about_us.setMenuRole(QAction.MenuRole.NoRole)   #add line if about doesnt show on the menu bar

        search_action = QAction(QIcon('icons/search.png'),"Search", self)
        search_menu.addAction(search_action)
        search_action.triggered.connect(self.search)

        #create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no'))
        self.setCentralWidget((self.table)) #append the table to the main window
        self.table.verticalHeader().setVisible(False) #removed duplicate index

        #create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True) #makes toolbar movable
        self.addToolBar(toolbar)

        #add elements to toolbar
        toolbar.addAction(add_student)
        toolbar.addAction(search_action)

        #create status bar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)





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

    def search(self):
        dialog = EditDialog()
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


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText('Enter Student Name')
        layout.addWidget(self.name)

        button = QPushButton('Submit')
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)



    def search(self):
        name = self.name.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString) #access table to find the name you search
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)
            cursor.close()
            connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.add_data()
sys.exit(app.exec())
