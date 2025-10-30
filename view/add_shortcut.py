import math
import sys
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal


from ui.add_shortcut import Ui_AddShortcut
from utils import Database


class AddShortcutView(QDialog, Ui_AddShortcut):
    add_shortcut_signal = pyqtSignal(dict)
    def __init__(self, parent=None):
        super(AddShortcutView, self).__init__(parent)
        self.setupUi(self)
        self.__init_ui()

    
    def __init_ui(self):
        """初始化UI"""
        self.setWindowModality(Qt.ApplicationModal)  # 模态对话框
        self.setFixedSize(self.size())  # 固定窗口大小，不能调整
        
        # 连接按钮信号
        self.btn_add.clicked.connect(self.handle_add)
        

    def __init_show(self):
        """在显示前的初始化"""
        # 清空输入框
        self.le_function.clear()
        self.le_shortcut.clear()
        self.te_note.clear()
        self.le_function.setFocus()  # 设置焦点到第一个输入框

    def handle_show(self):
        """显示对话框（模态）"""
        self.__init_show()
        self.exec_()  # 使用 exec_() 来实现模态对话框

    def handle_add(self):
        """处理添加按钮点击"""
        function = self.le_function.text().strip()
        shortcut = self.le_shortcut.text().strip()
        note = self.te_note.toPlainText().strip()

        if not function:
            QMessageBox.warning(self, "输入错误", "Function 不能为空")
            self.le_function.setFocus()
            return
        if not shortcut:
            QMessageBox.warning(self, "输入错误", "Shortcut key 不能为空")
            self.le_shortcut.setFocus()
            return

        self.add_shortcut_signal.emit({
            'function': function,
            'shortcut': shortcut,
            'note': note
        })

        self.close()
