from PyQt5.QtWidgets import QMainWindow
from ui.main import Ui_Main


class MainView(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.init_ui()
    
    def init_ui(self):
        pass

    def handle_show(self):
        self.show()

