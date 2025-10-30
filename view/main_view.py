
from PyQt5.QtWidgets import QMainWindow, QMenu, QMessageBox, QTableWidgetItem
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
        self.action_test1.triggered.connect(self.handle_test1)
        self.action_test2.triggered.connect(self.handle_test2)
        self.btn_add_name.clicked.connect(self.add_name)

        self.refresh_software_list()
        
        # 设置右键菜单
        self.lw_software_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_software_name.customContextMenuRequested.connect(self.show_context_menu)
        
        self.lw_software_name.itemDoubleClicked.connect(self.open_software)
        self.btn_home.clicked.connect(self.back_to_home)
        self.btn_add_shortcut.clicked.connect(self.add_shortcut)

    def handle_test1(self):
        print(Config.get_data("test"))        
    
    def handle_test2(self):
        print('--------')
        print(Database.getInstance().get_name_list())
    
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
                    QMessageBox.information(self, "删除成功", f"软件 '{software_name}' 已成功删除")
                else:
                    QMessageBox.warning(self, "删除失败", f"删除软件 '{software_name}' 时出现错误")

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
    
    def back_to_home(self):
        self.sw_main.setCurrentIndex(0)
        self.lb_software_name.setText("")
    
    def add_shortcut(self):
        self.add_shortcut_view = AddShortcutView()
        self.add_shortcut_view.add_shortcut_signal.connect(self.add_shortcut_signal)
        self.add_shortcut_view.handle_show()
    
    def add_shortcut_signal(self, data):
        print('data', data)
        function = data['function']
        shortcut = data['shortcut']
        note = data['note']
        Database.getInstance().insert_shortcut(self.software_id, function, shortcut, note)
        self.refresh_shortcut_table()
    
    def refresh_shortcut_table(self):
        """刷新快捷键表格"""
        # 清空表格
        self.tw_shortcut.clear()
        self.tw_shortcut.setRowCount(0)
        
        # 设置列数和列标题
        self.tw_shortcut.setColumnCount(2)
        self.tw_shortcut.setHorizontalHeaderLabels(["Function", "Keys"])
        
        # 设置行数
        row_count = len(self.shortcut_info)
        self.tw_shortcut.setRowCount(row_count)
        
        # 填充数据
        for row, (function, keys, note) in enumerate(self.shortcut_info):
            # function 列
            function_item = QtWidgets.QTableWidgetItem(function if function else "")
            self.tw_shortcut.setItem(row, 0, function_item)
            
            # keys 列
            keys_item = QtWidgets.QTableWidgetItem(keys if keys else "")
            self.tw_shortcut.setItem(row, 1, keys_item)
        
        # 设置列宽比例为 2:1
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

    def handle_show(self):
        self.show()

