import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QWidget,
    QStatusBar,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QToolBar,
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)

        # Create menu bar
        file_menu = self.menuBar().addMenu('&File')
        help_menu = self.menuBar().addMenu('&Help')
        search_menu = self.menuBar().addMenu('&Edit')

        # Create sub menu bar
        add_student = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)

        about_us = QAction('About', self)
        help_menu.addAction(about_us)
        about_us.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon('icons/search.png'), 'Search', self)
        search_menu.addAction(search_action)
        search_action.triggered.connect(self.search)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id', 'Name', 'Course', 'Mobile no'))
        self.setCentralWidget(self.table)
        self.table.verticalHeader().setVisible(False)

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Add elements to toolbar
        toolbar.addAction(add_student)
        toolbar.addAction(search_action)

        # Create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Add elements to statusbar (buttons)
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)
        button_exist = self.findChildren(QPushButton)
        if button_exist:
            for button in button_exist:
                self.statusBar().removeWidget(button)
        self.statusBar().addWidget(edit_button)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)
        self.statusBar().addWidget(delete_button)

    def add_data(self):
        connection = sqlite3.connect('database.db')
        result = connection.execute('SELECT * FROM students')
        self.table.setRowCount(0)
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

    def edit(self):
        dialog = EditStatusBarDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditStatusBarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()  #get student name from selected row
        self.name = QLineEdit(student_name)
        self.name.setPlaceholderText('Name')
        layout.addWidget(self.name)

        course_name = main_window.table.item(index, 2).text()
        self.courses = QComboBox()
        self.courses.addItems(['Biology', 'Maths', 'Chemistry', 'Physics'])
        self.courses.setCurrentText(course_name)
        layout.addWidget(self.courses)

        self.phone_no = QLineEdit()
        self.phone_no.setPlaceholderText('Phone No.')
        layout.addWidget(self.phone_no)

        button = QPushButton('Submit')
        button.clicked.connect(self.update)
        layout.addWidget(button)

        self.setLayout(layout)

    def update(self):
        pass

class DeleteDialog(QDialog):
    pass


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

        self.phone_no = QLineEdit()
        self.phone_no.setPlaceholderText('Phone No.')
        layout.addWidget(self.phone_no)

        button = QPushButton('Submit')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.name.text()
        course = self.courses.itemText(self.courses.currentIndex())
        mobile = self.phone_no.text()

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)', (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.add_data()
        self.close()


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
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            
            main_window.table.item(item.row(), 1).setSelected(True)
            cursor.close()
            connection.close()
        


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.add_data()
sys.exit(app.exec())
