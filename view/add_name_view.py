import math
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal


from ui.add_name import Ui_AddName
from utils import Database


class AddNameView(QWidget, Ui_AddName):
    add_signal = pyqtSignal(bool)
    def __init__(self, parent=None):
        super(AddNameView, self).__init__(parent)
        self.setupUi(self)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowFlags(
            Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.btn_cancel.clicked.connect(self.close)
        self.btn_add.clicked.connect(self.add_name)

    def add_name(self):
        name = self.le_name.text().strip()

        if not name:
            QMessageBox.warning(self, "警告", "请输入名称")
            self.le_name.setFocus()
            return
        saved_name_list =  Database.getInstance().get_name_list()
        if name in saved_name_list:
            QMessageBox.warning(self, "警告", "名称已存在")
            self.le_name.setFocus()
            return
        Database.getInstance().insert_name(name)
        self.add_signal.emit(True)
        self.close()

    def handle_show(self):
        self.show()
