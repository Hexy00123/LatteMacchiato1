import sys
import sqlite3
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None, type=None, args=None):
        super(Dialog, self).__init__(parent)
        Form = self
        Form.setObjectName("Form")
        Form.resize(343, 224)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 160, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 0, 181, 191))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.grade_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.grade_line.setObjectName("grade_line")
        self.verticalLayout_2.addWidget(self.grade_line)
        self.degree_of_roast_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.degree_of_roast_line.setObjectName("degree_of_roast_line")
        self.verticalLayout_2.addWidget(self.degree_of_roast_line)
        self.box = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.box.setObjectName("box")
        self.verticalLayout_2.addWidget(self.box)
        self.flavor_description_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.flavor_description_line.setObjectName("flavor_description_line")
        self.verticalLayout_2.addWidget(self.flavor_description_line)
        self.cost_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.cost_line.setObjectName("cost_line")
        self.verticalLayout_2.addWidget(self.cost_line)
        self.volume_line = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.volume_line.setObjectName("volume_line")
        self.verticalLayout_2.addWidget(self.volume_line)
        self.button = QtWidgets.QPushButton(Form)
        self.button.setGeometry(QtCore.QRect(260, 190, 81, 31))
        self.button.setObjectName("button")

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Название сорта"))
        self.label.setText(_translate("Form", "Степень обжарки"))
        self.label_2.setText(_translate("Form", "Молотый/в зернах"))
        self.label_7.setText(_translate("Form", "Описание вкуса"))
        self.label_5.setText(_translate("Form", "Цена"))
        self.label_6.setText(_translate("Form", "Объем упаковки"))
        self.button.setText(_translate("Form", "Записать"))
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.parent = parent
        self.type = type
        self.args = args

        self.box.addItems(['молотый', 'зерна'])

        self.con = sqlite3.connect("data/coffee.db")
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
        Form = self
        Form.setObjectName("Form")
        Form.resize(715, 424)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, 721, 381))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.change_button = QtWidgets.QPushButton(Form)
        self.change_button.setGeometry(QtCore.QRect(0, 0, 121, 41))
        self.change_button.setObjectName("change_button")
        self.add_button = QtWidgets.QPushButton(Form)
        self.add_button.setGeometry(QtCore.QRect(120, 0, 101, 41))
        self.add_button.setObjectName("add_button")

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.change_button.setText(_translate("Form", "Изменить запись"))
        self.add_button.setText(_translate("Form", "Добавить запись"))
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.con = sqlite3.connect("data/coffee.db")
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
