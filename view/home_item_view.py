from PyQt5.QtWidgets import QWidget
from ui.home_item import Ui_HomeItem


class HomeItemView(QWidget, Ui_HomeItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
    
    def init_ui(self):
        pass

    def handle_show(self):
        self.show()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = HomeItemView()
    window.handle_show()
    sys.exit(app.exec_())