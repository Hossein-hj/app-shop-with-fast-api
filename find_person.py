# code 3







from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem 
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from fast_database import Database

class Ui_find_person_dialog(QDialog):
    # def __init__(self):
    #     super().__init__()
    #     self.setupUi()
    #     self.custmer_list = []
    #     self.find_person()
    #     self.pushButton_select.setEnabled(False)
    #     self.active_user = None
    #     self.signals
    def __init__(self):

        super().__init__()

        self.setupUi()

        self.custmer_list = []

        self.active_user = None

        # عکس پیشفرض
        self.label_pic.setPixmap(QtGui.QPixmap("pic/nopic.jpg"))

        # دکمه غیرفعال
        self.pushButton_select.setEnabled(False)

        # سیگنال‌ها
        self.signals()

        # خواندن اطلاعات
        self.find_person()   


    # def signals(self):
    #     self.tableWidget_person.clicked.connect(self.active_change)
    #     self.lineEdit_name.textChanged.connect(self.find_person)
    #     self.lineEdit_id.textChanged.connect(self.find_person)
    #     self.tableWidget_person.clicked.connect(self.active_change)
    def signals(self):

        self.tableWidget_person.clicked.connect(self.active_change)

        self.lineEdit_name.textChanged.connect(self.find_person)

        self.lineEdit_id.textChanged.connect(self.find_person)


    def find_person(self):

        mydb = Database()

        data = mydb.find_customer(
            name=self.lineEdit_name.text(),
            id=self.lineEdit_id.text()
        )

        self.custmer_list = [
            {
                'Id': p[0],
                'Name': p[1],
                'pic': p[2]
            }
            for p in data
        ]

        self.fill_table()

        if rows := len(self.custmer_list):

            self.tableWidget_person.setCurrentCell(0, 0)

            self.active_change()

        else:

            self.label_pic.setPixmap(QtGui.QPixmap("nopic.jpg"))

            self.pushButton_select.setEnabled(False)

    def active_change(self):

        row = self.tableWidget_person.currentRow()

        if row < 0:
            return

        self.active_user = self.custmer_list[row]

        pic = self.active_user['pic']

        # اگر عکس وجود داشت
        if pic != '':

            self.label_pic.setPixmap(QtGui.QPixmap(pic))

        # اگر عکس نداشت
        else:

            self.label_pic.setPixmap(
                QtGui.QPixmap("pic/nopic.jpg")
            )

        self.pushButton_select.setEnabled(True)

        



    # def load_persons(self):
    #     mydb = Database()
    #     data = mydb.read_all_customers()
    #     print(data)
    #     self.custmer_list = [{'Id': p[0] , 'Name' : p[1] , 'pic' : p[2]}for p in data]
    #     self.fill_table()

    
    def fill_table(self):

        self.tableWidget_person.clear()

        columns = ['Id', 'Name', 'pic']

        rows = len(self.custmer_list)

        cols = len(columns)

        self.tableWidget_person.setRowCount(rows)

        self.tableWidget_person.setColumnCount(cols)

        self.tableWidget_person.setHorizontalHeaderLabels(columns)

        font = QtGui.QFont()

        font.setPointSize(12)

        font.setBold(True)

        for row in range(rows):

            person = self.custmer_list[row]

            values = [
                person['Id'],
                person['Name'],
                person['pic']
            ]

            for col in range(cols):

                item = QTableWidgetItem(str(values[col]))

                item.setTextAlignment(Qt.AlignCenter)

                item.setFont(font)

                item.setFlags(Qt.ItemIsEnabled)

                self.tableWidget_person.setItem(row, col, item)
    def find_person(self):

        mydb = Database()

        data = mydb.find_customer(
            name=self.lineEdit_name.text(),
            id=self.lineEdit_id.text()
        )

        self.custmer_list = [
            {
                'Id': p[0],
                'Name': p[1],
                'pic': p[2]
            }
            for p in data
        ]

        self.fill_table()

        # اگر کسی پیدا شد
        if len(self.custmer_list) > 0:

            self.tableWidget_person.setCurrentCell(0, 0)

            self.active_change()

    # اگر کسی پیدا نشد
        else:

            self.label_pic.setPixmap(
                QtGui.QPixmap("pic/nopic.jpg")
            )

            self.pushButton_select.setEnabled(False)






        # self.tableWidget_person.setVerticalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_person.setVerticalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_person.setVerticalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_person.setHorizontalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_person.setHorizontalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_person.setHorizontalHeaderItem(2, item)
        # item = QtWidgets.QTableWidgetItem()
        
    








    def setupUi(self):
        self.setObjectName("self")
        self.resize(672, 379)
        self.pushButton_select = QtWidgets.QPushButton(self)
        self.pushButton_select.setGeometry(QtCore.QRect(460, 330, 181, 28))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_select.setFont(font)
        self.pushButton_select.setObjectName("pushButton_select")
        self.tableWidget_person = QtWidgets.QTableWidget(self)
        self.tableWidget_person.setGeometry(QtCore.QRect(30, 80, 401, 271))
        self.tableWidget_person.setObjectName("tableWidget_person")
        self.tableWidget_person.setColumnCount(3)




        # self.tableWidget_person.setItem(0, 0, self.item )


        self.label_pic = QtWidgets.QLabel(self)
        self.label_pic.setGeometry(QtCore.QRect(450, 60, 211, 241))
        self.label_pic.setText("")
        self.label_pic.setPixmap(QtGui.QPixmap("nopic.jpg"))
        self.label_pic.setScaledContents(True)
        self.label_pic.setObjectName("label_pic")
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 331, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_name = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout.addWidget(self.lineEdit_name)
        self.label_id = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_id.setFont(font)
        self.label_id.setObjectName("label_id")
        self.horizontalLayout.addWidget(self.label_id)
        self.lineEdit_id = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.horizontalLayout.addWidget(self.lineEdit_id)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.pushButton_select.setText(_translate("self", "select"))
        # item = self.tableWidget_person.verticalHeaderItem(0)
        # item.setText(_translate("Dialog", "1"))
        # item = self.tableWidget_person.verticalHeaderItem(1)
        # item.setText(_translate("Dialog", "2"))
        # item = self.tableWidget_person.verticalHeaderItem(2)
        # item.setText(_translate("Dialog", "3"))
        # item = self.tableWidget_person.horizontalHeaderItem(0)
        # item.setText(_translate("Dialog", "Id"))
        # item = self.tableWidget_person.horizontalHeaderItem(1)
        # item.setText(_translate("Dialog", "Name"))
        # item = self.tableWidget_person.horizontalHeaderItem(2)
        # item.setText(_translate("Dialog", "pic"))
        __sortingEnabled = self.tableWidget_person.isSortingEnabled()
        self.tableWidget_person.setSortingEnabled(False)
        self.tableWidget_person.setSortingEnabled(__sortingEnabled)
        self.label_name.setText(_translate("self", "name:"))
        self.label_id.setText(_translate("self", "id:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    ui = Ui_find_person_dialog()
    
    ui.show()
    sys.exit(app.exec_())
