
from PyQt5.QtWidgets import QMainWindow
from ui.main import Ui_Main
from utils import Config, Database,Project


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
    
    def handle_test1(self):
        print(Config.get_data("test"))        
    
    def handle_test2(self):
        print("test2")  
        print(Project.get_project_path())

    def handle_show(self):
        self.show()

