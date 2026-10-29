import sys
from datetime import datetime
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from fast_database import Database


class Ui_open_factor_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.mydb = Database()
        self.active_factor = None
        self.all_factors = []
        self.setupUi()
        self.signals()
        self.fill_table()

    def signals(self):
        self.pushButton_search.clicked.connect(self.search_factor)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_open.clicked.connect(self.open_factor)
        self.tableWidget.cellClicked.connect(self.select_factor)
       
        self.lineEdit_search.textChanged.connect(self.search_factor)

    def fill_table(self):
        self.all_factors = list(self.mydb.read_all_factors() or [])
        self.search_factor()

    @staticmethod
    def normalize_date(value):
        value = str(value or '').strip().replace('-', '/')
        return value[:10]

    @staticmethod
    def to_number(value):
        try:
            return float(str(value).replace(',', '').strip())
        except (ValueError, TypeError):
            return None

    def search_factor(self, *_):
        date_from = self.normalize_date(self.lineEdit_date_from.text())
        date_to = self.normalize_date(self.lineEdit_date_to.text())
        price_from = self.to_number(self.lineEdit_price_from.text())
        price_to = self.to_number(self.lineEdit_price_to.text())
        query = self.lineEdit_search.text().strip().casefold()

        results = []
        for factor in self.all_factors:
            if len(factor) < 4:
                continue
            factor_id, customer, date_value, total = factor[0], factor[1], factor[2], factor[3]
            factor_date = self.normalize_date(date_value)
            amount = self.to_number(total)

            if query and query not in str(factor_id).casefold() and query not in str(customer).casefold():
                continue
            if date_from and factor_date < date_from:
                continue
            if date_to and factor_date > date_to:
                continue
            if price_from is not None and (amount is None or amount < price_from):
                continue
            if price_to is not None and (amount is None or amount > price_to):
                continue
            results.append(factor)

        self.show_result(results)

    def show_result(self, factors):
        self.tableWidget.setUpdatesEnabled(False)
        self.tableWidget.setRowCount(len(factors))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Factor ID", "Customer", "Date", "Total"])
        font = QtGui.QFont()
        font.setPointSize(11)
        for row, factor in enumerate(factors):
            for col in range(4):
                item = QTableWidgetItem(str(factor[col]))
                item.setFont(font)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tableWidget.setItem(row, col, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setUpdatesEnabled(True)
        self.active_factor = None
        self.pushButton_open.setEnabled(False)

    def select_factor(self, row, col):
        item = self.tableWidget.item(row, 0)
        if item:
            try:
                self.active_factor = int(item.text())
                self.pushButton_open.setEnabled(True)
            except ValueError:
                self.active_factor = None
                self.pushButton_open.setEnabled(False)

    def open_factor(self):
        if self.active_factor is not None:
            self.accept()

    def setupUi(self):
        self.resize(1000, 650)
        self.setWindowTitle("open factor")
        self.verticalLayout = QVBoxLayout(self)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Name or id customer"))
        self.lineEdit_search = QLineEdit()
        
        row1.addWidget(self.lineEdit_search)
        self.verticalLayout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("From date (YYYY/MM/DD):"))
        self.lineEdit_date_from = QLineEdit()
        row2.addWidget(self.lineEdit_date_from)
        row2.addWidget(QLabel("	To date:"))
        self.lineEdit_date_to = QLineEdit()
        row2.addWidget(self.lineEdit_date_to)
        self.verticalLayout.addLayout(row2)

        row3 = QHBoxLayout()
        row3.addWidget(QLabel("	Price from:"))
        self.lineEdit_price_from = QLineEdit()
        row3.addWidget(self.lineEdit_price_from)
        row3.addWidget(QLabel("	Price to:"))
        self.lineEdit_price_to = QLineEdit()
        row3.addWidget(self.lineEdit_price_to)
        self.verticalLayout.addLayout(row3)

        row4 = QHBoxLayout()
        self.pushButton_search = QPushButton("Search")
        self.pushButton_reset = QPushButton("Clear Filters")
        row4.addWidget(self.pushButton_search)
        row4.addWidget(self.pushButton_reset)
        self.verticalLayout.addLayout(row4)
        self.pushButton_reset.clicked.connect(self.reset_filters)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels([" Factor ID", "Customer", "Date", "Total"])
        self.tableWidget.horizontalHeader().setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalLayout.addWidget(self.tableWidget)

        row5 = QHBoxLayout()
        self.pushButton_open = QPushButton("open")
        self.pushButton_close = QPushButton("close")
        self.pushButton_open.setEnabled(False)
        row5.addWidget(self.pushButton_open)
        row5.addWidget(self.pushButton_close)
        self.verticalLayout.addLayout(row5)

    def reset_filters(self):
        for field in (self.lineEdit_search, self.lineEdit_date_from,
                      self.lineEdit_date_to, self.lineEdit_price_from,
                      self.lineEdit_price_to):
            field.clear()
        self.search_factor()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_open_factor_dialog()
    window.show()
    sys.exit(app.exec_())
