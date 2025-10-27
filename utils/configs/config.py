from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class Config:
    _instance = None

    _config = {
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set_data(cls, name, value):
        cls._config[name] = value

    @classmethod
    def get_data(cls, name, default=None):
        return cls._config.get(name, default)

    @classmethod
    def setOverrideCursor(cls):
        QApplication.setOverrideCursor(Qt.WaitCursor)

    @classmethod
    def resetOverrideCursor(cls):
        QApplication.restoreOverrideCursor()


