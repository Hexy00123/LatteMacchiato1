import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None, type=None, args=None):
        super(Dialog, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent = parent
        self.type = type
        self.args = args

        self.box.addItems(['молотый', 'зерна'])

        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()

        self.button.clicked.connect(self.f)

    def f(self):
        grade = self.grade_line.text()
        degree_of_roast = self.degree_of_roast_line.text()
        ground_beans = self.box.currentText()
        flavor_description = self.flavor_description_line.text()
        cost = self.cost_line.text()
        volume = self.volume_line.text()

        if self.type == 'add':
            data = self.cur.execute("""SELECT * FROM "table" """).fetchall()
            try:
                id = max(data, key=lambda x: x[0])[0] + 1
            except:
                id = 1
            self.cur.execute(f'''
                INSERT INTO 
                "table" (id, grade, degree_of_roast, ground_beans, flavor_description, cost, volume)
                VALUES
                ("{id}", "{grade}", "{degree_of_roast}", "{ground_beans}", 
                "{flavor_description}", "{cost}", "{volume}")
                ''')

        elif self.type == 'change':
            self.cur.execute(f'''
                UPDATE "table"
                SET grade = "{grade}",
                    degree_of_roast = "{degree_of_roast}",
                    ground_beans = "{ground_beans}",
                    flavor_description = "{flavor_description}",
                    cost = "{cost}",
                    volume = "{volume}"
                WHERE id = "{self.args}"
                ''')

        self.con.commit()
        self.parent.update_table()
        self.close()

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
        data = self.cur.execute('''SELECT * FROM "table" ''').fetchall()
        headers = [i[0] for i in self.cur.description]

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(len(data))

        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i in range(len(data)):
            for j in range(len(headers)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    def add(self):
        dialog = Dialog(self, 'add')
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()
        self.update_table()

    def change(self):
        self.tableWidget: QtWidgets.QTableWidget
        row = self.tableWidget.currentRow()
        id = self.tableWidget.item(row, 0).text()

        dialog = Dialog(self, 'change', id)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.show()
        self.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
