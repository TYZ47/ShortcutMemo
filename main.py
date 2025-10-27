import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, 
                            QPushButton, QLineEdit, QVBoxLayout, 
                            QWidget)


class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和大小
        self.setWindowTitle("简单PyQt5界面")
        self.setGeometry(100, 100, 400, 200)  # (x, y, 宽, 高)
        
        # 创建中心部件并设置布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标签
        self.label = QLabel("请输入内容：", self)
        layout.addWidget(self.label)
        
        # 添加输入框
        self.input_box = QLineEdit(self)
        layout.addWidget(self.input_box)
        
        # 添加按钮
        self.button = QPushButton("点击显示", self)
        self.button.clicked.connect(self.show_text)  # 绑定按钮点击事件
        layout.addWidget(self.button)
        
        # 添加显示结果的标签
        self.result_label = QLabel("", self)
        layout.addWidget(self.result_label)

    def show_text(self):
        """按钮点击事件处理函数：显示输入框中的内容"""
        text = self.input_box.text()
        if text:
            self.result_label.setText(f"你输入的是：{text}")
        else:
            self.result_label.setText("输入框为空，请输入内容")


if __name__ == "__main__":
    # 创建应用实例
    app = QApplication(sys.argv)
    # 创建并显示窗口
    window = SimpleGUI()
    window.show()
    # 进入应用主循环
    sys.exit(app.exec_())