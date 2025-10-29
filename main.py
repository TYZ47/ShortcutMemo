import sys

from PyQt5.QtCore import QDir, QLockFile
from PyQt5.QtWidgets import QApplication, QMessageBox

from view.main_view import MainView

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = MainView()
    main.handle_show()
    sys.exit(app.exec_())
