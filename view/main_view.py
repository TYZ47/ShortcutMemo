
from PyQt5.QtWidgets import QMainWindow, QMenu, QMessageBox
from PyQt5.QtCore import Qt
from ui.main import Ui_Main
from utils import Config, Database, Project
from view.add_name_view import AddNameView

class MainView(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.__init_confit()

        self.init_ui()

    def __init_confit(self):
        Database.getInstance()
    
    def init_ui(self):
        self.action_test1.triggered.connect(self.handle_test1)
        self.action_test2.triggered.connect(self.handle_test2)
        self.btn_add_name.clicked.connect(self.add_name)

        name_list = Database.getInstance().get_name_list()

        self.lw_software_name.clear()
        for name in name_list:
            self.lw_software_name.addItem(name)
        
        # 设置右键菜单
        self.lw_software_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_software_name.customContextMenuRequested.connect(self.show_context_menu)
        
        
    def handle_test1(self):
        print(Config.get_data("test"))        
    
    def handle_test2(self):
        print('--------')
        print(Database.getInstance().get_name_list())
    
    def add_name(self):
        self.add_name_view = AddNameView()
        self.add_name_view.handle_show()

    def show_context_menu(self, position):
        """显示右键菜单"""
        if self.lw_software_name.itemAt(position) is None:
            return
        
        # 创建右键菜单
        context_menu = QMenu(self)
        
        # 添加删除动作
        delete_action = context_menu.addAction("删除")
        delete_action.triggered.connect(self.delete_software)
        
        # 添加导出动作
        export_action = context_menu.addAction("导出")
        export_action.triggered.connect(self.export_software)
        
        # 显示菜单
        context_menu.exec_(self.lw_software_name.mapToGlobal(position))

    def delete_software(self):
        pass

    def export_software(self):
        pass

    def handle_show(self):
        self.show()

