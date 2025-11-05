import math
import sys
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QKeySequence


from ui.add_shortcut import Ui_AddShortcut
from utils import Database



# TODO 当我焦点在le_shortcut的时候，我在键盘上无论按下什么键，都用一个函数把它显示出来


class AddShortcutView(QDialog, Ui_AddShortcut):
    add_shortcut_signal = pyqtSignal(dict)
    def __init__(self, software_id: int, parent=None):
        super(AddShortcutView, self).__init__(parent)
        self.setupUi(self)
        self.software_id = software_id
        self.__init_ui()

    
    def __init_ui(self):
        """初始化UI"""
        self.setWindowModality(Qt.ApplicationModal)  # 模态对话框
        self.setFixedSize(self.size())  # 固定窗口大小，不能调整
        
        # 连接按钮信号
        self.btn_add.clicked.connect(self.handle_add)

        # 为快捷键输入框安装事件过滤器以捕获键盘输入
        self.le_shortcut.installEventFilter(self)

        

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
        shortcut_name_list = Database.getInstance().get_shortcut_name_by_id(self.software_id)
        if function in shortcut_name_list:
            QMessageBox.warning(self, "", "功能名称已存在")
            self.le_function.setFocus()
            return


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

    # --- 键盘捕获与显示 ---
    def eventFilter(self, obj, event):
        # 当焦点在 le_shortcut 上时，捕获键盘事件
        if obj is self.le_shortcut and event.type() == QEvent.KeyPress:
            return self._handle_shortcut_key_press(event)
        return super(AddShortcutView, self).eventFilter(obj, event)

    def _handle_shortcut_key_press(self, event):
        key = event.key()
        mods = event.modifiers()

        # 清空逻辑
        if key in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Escape):
            self.le_shortcut.clear()
            return True

        # 过滤掉仅修饰键（不生成序列）
        if key in (Qt.Key_Control, Qt.Key_Shift, Qt.Key_Alt, Qt.Key_Meta, Qt.Key_Super_L, Qt.Key_Super_R):
            return True

        # 合成 QKeySequence（PyQt5 需要把修饰键与主键进行或运算）
        combined = int(mods) | int(key)
        sequence = QKeySequence(combined)

        # 将本地化显示文本写入输入框
        text = sequence.toString(QKeySequence.NativeText)
        # 若生成结果为空（极少见），则不修改
        if text:
            self.le_shortcut.setText(text)

        return True
