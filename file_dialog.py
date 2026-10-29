import sys
from PyQt5.QtWidgets import QApplication , QWidget , QFileDialog

class file_open_dialog(QWidget):
    def __init__(self):
        super().__init__()
    
    def open_file_dialog(self):
        # options = QFileDialog.Options()
        # options
        fileName , _ = QFileDialog.getOpenFileName(self,caption="Find image" ,directory="" , filter="All Files (*);;jpg (*.jpg);;PNG (*.pNG);;" )
        # directory = masir entekhab file
        if fileName:
            return fileName
        else:
            return None