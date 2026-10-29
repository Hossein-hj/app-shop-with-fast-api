from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem , QMessageBox
from enter_pro import Ui_Dialoginputprice
from new_person import Ui_new_personDialog
from PyQt5.QtCore import Qt
from find_person import Ui_find_person_dialog
from fast_database import Database
from edite_products import Ui_Dialog_Editproduct
from delete_products import Ui_Dialog_delete_product
from open_factor_last import Ui_open_factor_dialog
import jdatetime


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mydb = Database()
        self.products = [{'id':-1,'name':'please select..','price':0},]
        self.customer_id = None
        self.factor_id = None
        self.total = 0
        self.factor_dirty = False

        self.today =  jdatetime.date.today().strftime('%Y/%m/%d')
        
        now = jdatetime.datetime.now().strftime('%Y/%m/%d - %H:%M')
        
        self.factor_list = []

        
        
    def my_signals(self):
        self.pushButtonadd.clicked.connect(self.add_to_list)
        self.comboBoxPname.currentIndexChanged.connect(self.active_btn_add)
        self.spinBoxNo.valueChanged.connect(self.active_btn_add)
        self.tableWidget.clicked.connect(self.change_item)
        self.actionaddproduct.triggered.connect(self.new_product)
        self.actionedit_product.triggered.connect(self.edit_product)
        self.actiondel_All_product.triggered.connect(self.delete_all_products)
        self.actionaddperson.triggered.connect(self.new_person)
        self.actiondel_product.triggered.connect(self.del_product)
        self.action_find_person.triggered.connect(self.find_customer)
        self.pushButton_save.clicked.connect(self.save_factor)
        self.actionEXIT.triggered.connect(self.close_app)
        self.actionnew_factor.triggered.connect(self.new_factor)
        self.actionsave_factor.triggered.connect(self.save_factor)
        self.actionopen.triggered.connect(self.open_factor)
        
    def close_app(self):
        self.close()

    def new_factor(self):
        self.factor_list = []
        self.show_table()
        self.total = 0
        self.lineEdit_total.setText("0")
        self.customer_id = 0
        self.label.setText("No customer selected")
        self.factor_id = 0
        self.factor_dirty = False
        self.pushButton_save.setEnabled(False)
        self.actionsave_factor.setEnabled(False)


    def open_factor(self):

        if self.factor_list and self.factor_dirty:

            msg = QMessageBox(self)
            msg.setWindowTitle("Save Factor")
            msg.setText(
                "The current invoice has unsaved changes.\n"
                "Would you like to save it before continuing?"
            )

            btn_yes = msg.addButton(
                "Save factor",
                QMessageBox.YesRole
            )
            btn_no = msg.addButton(
                " Dont Save",
                QMessageBox.NoRole
            )
            btn_cancel = msg.addButton(
                "Close",
                QMessageBox.RejectRole
            )

            msg.exec_()
            clicked = msg.clickedButton()

            if clicked == btn_cancel:
                return

            if clicked == btn_yes:
                self.save_factor()

                
                if self.factor_dirty:
                    return

            elif clicked == btn_no:
                pass

        ui = Ui_open_factor_dialog()

        if ui.exec():
            factor_id = ui.active_factor
            self.load_factor(factor_id)
    
    def load_factor(self, factor_id):

        factor, details = self.mydb.read_factor(factor_id)

        self.factor_id = factor_id

        self.customer_id = factor["customer_id"]

        self.label.setText(
            f"{factor['customer_name']} - {self.customer_id}"
        )

        self.factor_list = []

        for row in details:

            self.factor_list.append({
                "id": row["product_id"],
                "name": row["product_name"],
                "price": row["price"],
                "No": row["count"],
                "Total": row["total"]
            })
            self.factor_dirty = False
        self.show_table()

    
    def save_factor(self):

        if self.customer_id:

            self.pushButton_save.setEnabled(False)
            self.actionsave_factor.setEnabled(False)

            if self.factor_id:

                ok = self.mydb.update_factor(
                    customer_id=self.customer_id,
                    total=self.total,
                    factor_id=self.factor_id
                )

                if ok is not None:
                    ok = self.mydb.update_factor_details(
                        factor_id=self.factor_id,
                        factor_list=self.factor_list
                    )

            else:

                new_id = self.mydb.create_new_factor(
                    customer_id=self.customer_id,
                    date=jdatetime.datetime.now().strftime('%Y/%m/%d - %H:%M'),
                    total=self.total
                )

                ok = None
                if new_id is not None:
                    self.factor_id = new_id
                    ok = self.mydb.save_factor_details(
                        factor_id=self.factor_id,
                        factor_list=self.factor_list
                    )

            if ok is None:
                # ذخیره نشد: دکمه‌ها رو دوباره فعال می‌کنیم و پیام می‌دیم
                self.pushButton_save.setEnabled(True)
                self.actionsave_factor.setEnabled(True)
                QMessageBox.warning(
                    self,
                    "warning",
                    "factor was not saved (check the API server and the customer)"
                )
                return

            self.factor_dirty = False
            QMessageBox.information(
                self,
                "success",
                "factor saved"
            )

        else:

            QMessageBox.warning(
                self,
                "warning",
                "please select customer"
            )

    def find_customer(self):
        ui = Ui_find_person_dialog()
        ui.pushButton_select.clicked.connect(lambda:self.find_person(ui))
        ui.exec_()


    def find_person(self, ui):
        self.customer_id = ui.active_user['Id']

        customer_name = ui.active_user['Name']

        
        self.label.setText(
            f"{customer_name} - {self.customer_id}"
        )
        ui.close()

    def del_product(self):
        ui = Ui_Dialog_delete_product()
        ui.setupUi()
        id = ui.lineEdit_id.text()
        result = self.mydb.read_products_by_id(id=id)
        
        
        if result:
            self.mydb.delete_product_by_id(id=id)
            self.fill_combobox()
            ui.close()
        else:
            ui.label_error.setText(" No data found ")

        

        ui.exec_()

    def delete_all_products(self):
        self.mydb.delete_all_products()
        self.fill_combobox()
    def new_person(self):
        self.ui_person = Ui_new_personDialog()
       
        self.ui_person.pushButton_add.clicked.connect(self.add_new_person)
        self.ui_person.show()





    def add_new_person(self):

        user_name = self.ui_person.lineEdit_username.text()

        pic = self.ui_person.img

      
        password = self.ui_person.lineEdit_password.text()

        customer_id = self.mydb.create_new_person(
            name=user_name,
            pic=pic,
            password=password
        )

        if customer_id is None:
            QMessageBox.warning(
                self,
                "warning",
                "could not add the customer (is the API server running?)"
            )
            return

       
        self.customer_id = customer_id

    
        self.label.setText(
            f"{user_name} - {self.customer_id}"
        )

      
        self.ui_person.close()


    def new_product(self):
        ui = Ui_Dialoginputprice()
        ui.setupUi()
        ui.pushButtonsave.setEnabled(ui.lineEdit_name != '' and ui.label_id != '')
        self.products = list(self.products)
        ui.label_id.setText(str(len(self.products)))
        ui.pushButtonsave.clicked.connect(lambda:self.add_new_product(ui))
        ui.setWindowTitle(f'add item {len(self.products)}')
        ui.exec_()

    def add_new_product(self , myui:Ui_Dialoginputprice):
        
        # id == myui.labelid.text()
        self.mydb.create_new_products(name=myui.lineEdit_name.text() , price=myui.lineEdit_price.text() )
        
        self.fill_combobox()
        myui.close()


    def edit_product(self):
        ui = Ui_Dialog_Editproduct()
        ui.setupUi()
        
        ui.pushButtonsave.clicked.connect(lambda:self.edit_old_product(ui))
        ui.pushButtonsave.clicked.connect(ui.my_update)
        ui.exec_()

    def edit_old_product(self , myui:Ui_Dialog_Editproduct):
        # self.comboBoxPname.clear()
        self.fill_combobox()
        myui.close()



    def del_product(self):
        ui = Ui_Dialog_delete_product()
        ui.setupUi()
        
        # ui.pushButtonsave.clicked.connect(lambda:self.del_old_product(ui))
        ui.pushButtonsave.clicked.connect(ui.del_product)
        self.comboBoxPname.clear()
        self.fill_combobox()
        ui.exec_()
    
    # def del_old_product(self , myui:Ui_Dialog_delete_product):
        
    #     myui.close()



    def change_item(self):

        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()

        if row < 0:
            return

        # Add
        if col == 5:

            self.factor_list[row]['No'] += 1

            self.factor_list[row]['Total'] = (
                self.factor_list[row]['No']
                * self.factor_list[row]['price']
            )

        # Delete
        elif col == 6:
            self.factor_dirty = True
            self.factor_list[row]['No'] -= 1

            if self.factor_list[row]['No'] <= 0:

                self.factor_list.pop(row)

            else:

                self.factor_list[row]['Total'] = (
                    self.factor_list[row]['No']
                    * self.factor_list[row]['price']
                )

        else:
            return

        self.pushButton_save.setEnabled(True)
        self.actionsave_factor.setEnabled(True)

        self.show_table()

    def active_btn_add(self):
        self.pushButtonadd.setEnabled(self.spinBoxNo.value() != 0 and self.comboBoxPname.currentIndex() != 0)

    
    def fill_combobox(self):

   
        self.products = [
            {'id': -1, 'name': 'please select...', 'price': 0}
        ]

       
        result = self.mydb.read_all_products()

        for p in result:

            item = {
                'id': p[0],
                'name': p[1],
                'price': p[2]
            }

            self.products.append(item)

        
        self.comboBoxPname.clear()

        
        for item in self.products:

            self.comboBoxPname.addItem(item['name'])


    
    def add_to_list(self):

        index = self.comboBoxPname.currentIndex()

        # جلوگیری از خطا
        if index <= 0:
            return

        data = self.products[index]

        No = self.spinBoxNo.value()

        if No <= 0:
            return

        new_row = {
            'id': data['id'],
            'name': data['name'],
            'price': data['price'],
            'No': No,
            'Total': data['price'] * No
        }

        found = False

        for row in self.factor_list:

            if row['id'] == new_row['id']:

                row['No'] += No

                row['Total'] += new_row['Total']

                found = True

                break

        if not found:

            self.factor_list.append(new_row)

            self.factor_dirty = True
        

        





        self.pushButton_save.setEnabled(True)
        self.actionsave_factor.setEnabled(True)

        self.show_table()
    def show_table(self):

        columns = ['id', 'name', 'No', 'price', 'Total', 'Add', 'Delete']

        rows = len(self.factor_list)
        cols = len(columns)

        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(cols)
        self.tableWidget.setHorizontalHeaderLabels(columns)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        total_all = 0

        for row in range(rows):

            item_data = self.factor_list[row]

            total_all += item_data['Total']

            values = [
                item_data['id'],
                item_data['name'],
                item_data['No'],
                item_data['price'],
                item_data['Total']
            ]

            # ستون های اصلی
            for col in range(5):

                item = QTableWidgetItem(str(values[col]))
                item.setFont(font)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(Qt.ItemIsEnabled)

                self.tableWidget.setItem(row, col, item)

            # Add
            item_add = QTableWidgetItem("Add")
            item_add.setFont(font)
            item_add.setTextAlignment(Qt.AlignCenter)
            item_add.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            self.tableWidget.setItem(row, 5, item_add)

            # Delete
            item_del = QTableWidgetItem("Delete")
            item_del.setFont(font)
            item_del.setTextAlignment(Qt.AlignCenter)
            item_del.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

            self.tableWidget.setItem(row, 6, item_del)

        # مجموع فاکتور
        self.total = total_all
        self.lineEdit_total.setText(str(total_all))

        self.comboBoxPname.setCurrentIndex(0)
        self.spinBoxNo.setValue(0)

    def setupUi(self):
        self.font_big = QtGui.QFont()
        self.font_big.setPointSize(16)
        self.font_big.setBold(True)
        self.setObjectName("MainWindow")
        self.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 10, 611, 170))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBoxcustomer = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBoxcustomer.setObjectName("groupBoxcustomer")
        font_group = QtGui.QFont()
        font_group.setPointSize(9)
        font_group.setBold(True)
        self.groupBoxcustomer.setFont(font_group)
        self.label = QtWidgets.QLabel(self.groupBoxcustomer)
        self.label.setGeometry(QtCore.QRect(30, 27, 250,30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)




        
        self.verticalLayout.addWidget(self.groupBoxcustomer)
        self.groupboxproduct = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupboxproduct.setMinimumSize(QtCore.QSize(200, 10))
        self.groupboxproduct.setObjectName("groupboxproduct")
        self.groupboxproduct.setFont(font_group)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupboxproduct)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelname = QtWidgets.QLabel(self.groupboxproduct)
        self.labelname.setMinimumSize(QtCore.QSize(49, 49))
        self.labelname.setMaximumSize(QtCore.QSize(49, 49))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelname.setFont(font)
        self.labelname.setObjectName("labelname")
        self.horizontalLayout.addWidget(self.labelname)
        self.comboBoxPname = QtWidgets.QComboBox(self.groupboxproduct)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBoxPname.setFont(font)
        self.comboBoxPname.setObjectName("comboBoxPname")
        self.comboBoxPname.setMinimumSize(QtCore.QSize(180, 30))
        self.comboBoxPname.setMaximumSize(QtCore.QSize(180, 30))
        
        


        self.horizontalLayout.addWidget(self.comboBoxPname)
        self.labelNo = QtWidgets.QLabel(self.groupboxproduct)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelNo.setFont(font)
        self.labelNo.setObjectName("labelNo")
        self.horizontalLayout.addWidget(self.labelNo)
        self.spinBoxNo = QtWidgets.QSpinBox(self.groupboxproduct)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxNo.sizePolicy().hasHeightForWidth())
        self.spinBoxNo.setSizePolicy(sizePolicy)
        self.spinBoxNo.setMinimumSize(QtCore.QSize(150, 20))
        self.spinBoxNo.setMaximumSize(QtCore.QSize(150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBoxNo.setFont(font)
        self.spinBoxNo.setObjectName("spinBoxNo")
        self.horizontalLayout.addWidget(self.spinBoxNo)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.pushButtonadd = QtWidgets.QPushButton(self.groupboxproduct)
        self.pushButtonadd.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonadd.setObjectName("pushButtonadd")
        self.horizontalLayout_2.addWidget(self.pushButtonadd)
        self.verticalLayout.addWidget(self.groupboxproduct)

        self.lineEdit_total = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_total.setGeometry(QtCore.QRect(780, 600, 170, 50))
        self.lineEdit_total.setObjectName("lineEdit_total")
        self.lineEdit_total.setReadOnly(True)  
        self.lineEdit_total.setFont(font_group) 

        
        
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setText("Save")
        self.pushButton_save.setGeometry(1000,600,90,50)
        self.pushButton_save.setEnabled(False)
        self.pushButton_save.setFont(font)
        # self.pushButton_save.setStyleSheet(
        #     "background-color: green;"
        #     "color: white;"
        # )
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(150, 210, 910, 301))
        self.tableWidget.setObjectName("tableWidget")
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.setCentralWidget(self.centralwidget)

        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menuproduct = QtWidgets.QMenu(self.menubar)
        self.menuproduct.setObjectName("menuproduct")
        self.menuperson = QtWidgets.QMenu(self.menubar)
        self.menuperson.setObjectName("menuperson")

        
        
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionnew_factor = QtWidgets.QAction(self)
        self.actionnew_factor.setObjectName("actionnew_factor")
        self.actionsave_factor = QtWidgets.QAction(self)
        self.actionsave_factor.setObjectName("actionsave_factor")
        self.actionsave_factor.setEnabled(False)

        self.actionaddproduct= QtWidgets.QAction(self)
        self.actionaddproduct.setObjectName("actionnew_product")
        self.actionedit_product= QtWidgets.QAction(self)
        self.actionedit_product.setObjectName("actionedit_product")
        self.actiondel_product= QtWidgets.QAction(self)
        self.actiondel_product.setObjectName("actiondel_product")
        self.actiondel_product.setText("delete product")
        self.actiondel_All_product= QtWidgets.QAction(self)
        self.actiondel_All_product.setObjectName("actiondel_All_product")
        self.actiondel_All_product.setText("delete All product")
        self.action_find_person= QtWidgets.QAction(self)
        self.action_find_person.setObjectName("action_find_person")
        self.action_find_person.setText("SELECT person")
        
        self.actionaddperson= QtWidgets.QAction(self)
        self.actionaddperson.setObjectName("actionnew_person")




        self.actionopen = QtWidgets.QAction(self)
        self.actionopen.setObjectName("actionopen")
        self.actionEXIT = QtWidgets.QAction(self)
        self.actionEXIT.setObjectName("actionEXIT")
        self.menufile.addAction(self.actionnew_factor)
        self.menufile.addAction(self.actionsave_factor)
        self.menufile.addAction(self.actionopen)
        self.menufile.addAction(self.actionnew_factor)



        self.menuproduct.addAction(self.actionaddproduct)
        self.menuproduct.addAction(self.actionedit_product)
        self.menuproduct.addAction(self.actiondel_product)
        self.menuproduct.addAction(self.actiondel_All_product)
        self.menuperson.addAction(self.actionaddperson)
        self.menuperson.addAction(self.action_find_person)
        
        


        self.menufile.addSeparator()
        self.menufile.addAction(self.actionEXIT)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuproduct.menuAction())
        self.menubar.addAction(self.menuperson.menuAction())

        
        self.retranslateUi()
        self.my_signals()
        self.fill_combobox()
        self.show_table()
        
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxcustomer.setTitle(_translate("MainWindow", "customer"))
        self.label.setText(_translate("MainWindow", "No customer selected"))
        self.groupboxproduct.setTitle(_translate("MainWindow", "product"))
        self.labelname.setText(_translate("MainWindow", "name:"))
     
        self.labelNo.setText(_translate("MainWindow", "No:"))
        self.pushButtonadd.setText(_translate("MainWindow", "add"))
        
        self.menufile.setTitle(_translate("MainWindow", "file"))
        self.menuproduct.setTitle(_translate("MainWindow", "product"))
        self.menuperson.setTitle(_translate("MainWindow", "person"))
        self.actionnew_factor.setText(_translate("MainWindow", "new factor"))
        self.actionsave_factor.setText(_translate("MainWindow", "save factor"))
        self.actionopen.setText(_translate("MainWindow", "open...."))
        self.actionEXIT.setText(_translate("MainWindow", "EXIT"))
        self.actionaddperson.setText(_translate("self","ADD person"))
        self.actionaddproduct.setText(_translate("self","ADD product"))
        self.actionedit_product.setText(_translate("self","Edit product"))
        


    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())