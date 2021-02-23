import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()

        self.add_button.clicked.connect(self.add)
        self.change_button.clicked.connect(self.change)

        self.update_table()

    def update_table(self):
        data = self.cur.execute("""SELECT * FROM "table" """).fetchall()
        headers = [i[0] for i in self.cur.description]

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(len(data))

        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i in range(len(data)):
            for j in range(len(headers)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def add(self):
        print('добавить')

    def change(self):
        print('изменить')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
