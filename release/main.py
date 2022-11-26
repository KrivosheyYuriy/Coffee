import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from main_window import Ui_MainWindow as form1
from addition import Ui_MainWindow as form2


class MainWindow(QMainWindow, form1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show_info()
        self.pushButton.clicked.connect(self.change_form)
        self.new = None
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def show_info(self):
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(('ID', 'название сорта', 'степень обжарки',
                                                    'молотый/в зернах', 'описание вкуса', 'цена',
                                                    'объем упаковки (граммов)'))
        data = cur.execute('SELECT * FROM coffee').fetchall()
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def change_form(self):
        self.new = Addition()
        self.new.show()
        self.hide()


class Addition(QMainWindow, form2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_info)
        self.molot.setChecked(True)
        self.Main_window = None

    def add_info(self):
        try:
            name = self.name.text()
            price = float(self.price.text())
            volume = int(self.volume.text())
            objarka = self.comboBox.currentText()
            desc = self.descr.toPlainText()
            if self.zern.isChecked():
                tip = 'В зернах'
            else:
                tip = 'Молотый'
            necessary_data = (name, objarka, tip, price, volume)
            assert all(necessary_data)
            new_id = max((x[0] for x in cur.execute('SELECT ID FROM coffee').fetchall())) + 1
            cur.execute(f'INSERT INTO coffee VALUES({new_id}, "{name}", "{objarka}", "{tip}", '
                        f'"{desc}", {price}, {volume})')
            con.commit()
            self.Main_window = MainWindow()
            self.Main_window.show()
            self.hide()
        except AssertionError:
            self.statusbar.setStyleSheet('Background-color: red')
            self.statusbar.showMessage('Введены не все обязательные данные!')
        except ValueError:
            self.statusbar.setStyleSheet('Background-color: red')
            self.statusbar.showMessage('Введены некорректные данные!')


if __name__ == '__main__':
    con = sqlite3.connect('Data/coffee.sqlite')
    cur = con.cursor()
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
