
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

        self.refresh_software_list()
        
        # 设置右键菜单
        self.lw_software_name.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_software_name.customContextMenuRequested.connect(self.show_context_menu)
        
        self.lw_software_name.itemDoubleClicked.connect(self.open_software)
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
        print('open software')
        pass

    def handle_show(self):
        self.show()

