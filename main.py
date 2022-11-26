import sys
import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.show_info()

    def show_info(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(('ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки (граммов)'))
        data = cur.execute('SELECT * FROM coffee').fetchall()
        self.tableWidget.setRowCount(1)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


if __name__ == '__main__':
    con = sqlite3.connect('coffee.sqlite')
    cur = con.cursor()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
