from PyQt5.QtWidgets import QMainWindow, QMenu, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from ui.main import Ui_Main
from utils import Config, Database, Project
from view.add_name_view import AddNameView
from view.add_shortcut import AddShortcutView


class MainView(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.__init_confit()

        self.init_ui()

    def __init_confit(self):
        Database.getInstance()

    def init_ui(self):
        self.sw_main.setCurrentIndex(0)
        self.shortcut_info = []
        self.software_id = None

        self.btn_add_name.clicked.connect(self.add_name)

        self.refresh_software_list()

        # 设置右键菜单
        self.lw_software_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_software_name.customContextMenuRequested.connect(
            self.show_context_menu)

        self.lw_software_name.itemDoubleClicked.connect(self.open_software)
        self.btn_home.clicked.connect(self.back_to_home)
        self.btn_add_shortcut.clicked.connect(self.add_shortcut)
        self.tw_shortcut.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_shortcut.itemClicked.connect(self.handle_item_clicked)
        self.tw_shortcut.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_shortcut.customContextMenuRequested.connect(self.show_shortcut_context_menu)

        self.btn_show_all.clicked.connect(self.show_all)
        self.btn_hide_all.clicked.connect(self.hide_all)

    def add_name(self):
        self.add_name_view = AddNameView()
        self.add_name_view.add_signal.connect(self.refresh_software_list)
        self.add_name_view.handle_show()

    def refresh_software_list(self):
        name_list = Database.getInstance().get_name_list()
        self.lw_software_name.clear()
        for name in name_list:
            self.lw_software_name.addItem(name)

    def show_context_menu(self, position):
        """显示右键菜单"""
        if self.lw_software_name.itemAt(position) is None:
            return

        # 创建右键菜单
        context_menu = QMenu(self)

        # 添加删除动作
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_software)

        # 添加导出动作
        export_action = context_menu.addAction("Export...")
        export_action.triggered.connect(self.export_software)

        # 显示菜单
        context_menu.exec_(self.lw_software_name.mapToGlobal(position))

    def delete_software(self):
        current_item = self.lw_software_name.currentItem()
        if current_item:
            software_name = current_item.text()
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除软件 '{software_name}' 吗？\n这将同时删除该软件的所有快捷键记录。",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                success = Database.getInstance().delete_name(software_name)
                if success:
                    self.refresh_software_list()
                    QMessageBox.information(
                        self, "删除成功", f"软件 '{software_name}' 已成功删除")
                else:
                    QMessageBox.warning(
                        self, "删除失败", f"删除软件 '{software_name}' 时出现错误")

    def export_software(self):
        pass

    def open_software(self):
        current_item = self.lw_software_name.currentItem()
        if current_item:
            software_name = current_item.text()
            software_id = Database.getInstance().get_id_by_name(software_name)

            shortcut_info = Database.getInstance().get_shortcut_info_by_id(software_id)
            self.software_id = software_id
            self.shortcut_info = shortcut_info
            print('shortcut_info', shortcut_info)
            self.sw_main.setCurrentIndex(1)
            self.lb_software_name.setText(software_name)
            self.refresh_shortcut_table()

    def back_to_home(self):
        self.sw_main.setCurrentIndex(0)
        self.lb_software_name.setText("")

    def add_shortcut(self):
        self.add_shortcut_view = AddShortcutView(self.software_id)
        self.add_shortcut_view.add_shortcut_signal.connect(
            self.add_shortcut_signal)
        self.add_shortcut_view.handle_show()

    def delete_shortcut(self):
        current_item = self.tw_shortcut.currentItem()
        if current_item:

            # todo 提示用户是否删除
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除快捷键 '{current_item.text()}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                row = current_item.row()
                function_item = self.tw_shortcut.item(row, 0)  # 获取这一行的第一列
                if function_item:
                    function = function_item.text()
                    success = Database.getInstance().delete_shortcut(self.software_id, function)
                    if success:
                        self.refresh_shortcut_table()
                    else:
                        QMessageBox.warning(self, "删除失败", "删除快捷键失败")

    def show_shortcut_context_menu(self, position):
        """显示快捷键表格的右键菜单"""
        item = self.tw_shortcut.itemAt(position)
        if item is None:
            return

        # 确保当前选中项是右键点击的行
        self.tw_shortcut.setCurrentItem(item)
        self.tw_shortcut.selectRow(item.row())

        context_menu = QMenu(self)
        delete_action = context_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_shortcut)
        context_menu.exec_(self.tw_shortcut.viewport().mapToGlobal(position))

    def add_shortcut_signal(self, data):
        print('data', data)
        function = data['function']
        shortcut = data['shortcut']
        note = data['note']

        success = Database.getInstance().insert_shortcut(
            self.software_id, function, shortcut, note)
        if success:
            self.refresh_shortcut_table()
        else:
            QMessageBox.warning(self, "添加失败", "添加快捷键失败")

    def refresh_shortcut_table(self):
        """刷新快捷键表格"""
        if not self.software_id:
            return

        self.shortcut_info = Database.getInstance(
        ).get_shortcut_info_by_id(self.software_id)

        self.tw_shortcut.clear()
        self.tw_shortcut.setRowCount(0)

        self.tw_shortcut.setColumnCount(2)
        self.tw_shortcut.setHorizontalHeaderLabels(["Function", "Keys"])

        row_count = len(self.shortcut_info)
        self.tw_shortcut.setRowCount(row_count)

        for row, (function, keys, note) in enumerate(self.shortcut_info):
            # function 列
            function_item = QtWidgets.QTableWidgetItem(
                function if function else "")
            self.tw_shortcut.setItem(row, 0, function_item)

            # keys 列
            keys_item = QtWidgets.QTableWidgetItem(keys if keys else "")
            self.tw_shortcut.setItem(row, 1, keys_item)

        header = self.tw_shortcut.horizontalHeader()
        total_width = self.tw_shortcut.width()
        if total_width > 0:
            self.tw_shortcut.setColumnWidth(0, int(total_width * 2 / 3))
            self.tw_shortcut.setColumnWidth(1, int(total_width * 1 / 3))
        else:
            # 如果表格还没有宽度，设置拉伸模式
            header.setStretchLastSection(False)
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def handle_item_clicked(self, item):
        """当点击快捷键表格中的某一行时，将该行选中（当这行的keys被清空时，这行的keys会显示出来）"""
        row = item.row()
        
        # 选中整行
        self.tw_shortcut.selectRow(row)
        
        # 如果这行的keys被清空了，需要恢复显示
        keys_item = self.tw_shortcut.item(row, 1)
        if keys_item and not keys_item.text().strip():
            # 获取该行的function
            function_item = self.tw_shortcut.item(row, 0)
            if function_item:
                function = function_item.text()
                # 从shortcut_info中找到对应的keys
                for func, keys, note in self.shortcut_info:
                    if func == function:
                        keys_item.setText(keys if keys else "")
                        break

    def show_all(self):
        """显示所有快捷键，第二列全部显示出来"""
        # 遍历所有行，恢复keys列的内容
        for row in range(self.tw_shortcut.rowCount()):
            function_item = self.tw_shortcut.item(row, 0)
            if function_item:
                function = function_item.text()
                # 从shortcut_info中找到对应的keys
                for func, keys, note in self.shortcut_info:
                    if func == function:
                        keys_item = self.tw_shortcut.item(row, 1)
                        if keys_item:
                            keys_item.setText(keys if keys else "")
                        else:
                            # 如果keys_item不存在，创建一个
                            keys_item = QtWidgets.QTableWidgetItem(keys if keys else "")
                            self.tw_shortcut.setItem(row, 1, keys_item)
                        break

    def hide_all(self):
        """隐藏所有快捷键，只显示第一列（Function），第二列（Keys）清空"""
        # 遍历所有行，清空keys列的内容
        for row in range(self.tw_shortcut.rowCount()):
            keys_item = self.tw_shortcut.item(row, 1)
            if keys_item:
                keys_item.setText("")
            else:
                # 如果keys_item不存在，创建一个空项
                keys_item = QtWidgets.QTableWidgetItem("")
                self.tw_shortcut.setItem(row, 1, keys_item)

    def handle_show(self):
        self.show()
