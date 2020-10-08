# -*- coding: utf-8 -*-
# AdminHome.py
# @author 灏喆
# @description 管理员主页
# @created 2019-05-25T16:27:43.374Z+08:00
# @last-modified 2019-06-13T11:24:30.861Z+08:00
#

import sys

from PyQt5.Qt import *

from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from BookStorageViewer import BookStorageViewer
from UserManage import UserManage


class AdminHome(QWidget):
    """
    管理员主页
    """

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        """
        Ui界面
        """
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.userManageButton = QPushButton("用户管理")
        self.addBookButton = QPushButton("添加书籍")
        self.dropBookButton = QPushButton("淘汰书籍")
        self.userManageButton.setFont(font)
        self.addBookButton.setFont(font)
        self.dropBookButton.setFont(font)
        self.userManageButton.setFixedWidth(100)
        self.userManageButton.setFixedHeight(42)
        self.addBookButton.setFixedWidth(100)
        self.addBookButton.setFixedHeight(42)
        self.dropBookButton.setFixedWidth(100)
        self.dropBookButton.setFixedHeight(42)
        self.buttonlayout.addWidget(self.addBookButton)
        self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.userManageButton)
        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.userManageButton.clicked.connect(self.userManage)

    def addBookButtonClicked(self):
        """
        弹出添加书籍对话框
        """
        addDialog = addBookDialog(self)
        addDialog.add_book_success_signal.connect(
            self.storageView.searchButtonClicked)  # 添加成功后刷新页面
        addDialog.show()
        addDialog.exec_()

    def dropBookButtonClicked(self):
        """
        弹出删除书籍对话框
        """
        dropDialog = dropBookDialog(self)
        dropDialog.drop_book_successful_signal.connect(
            self.storageView.searchButtonClicked)  # 添加成功后刷新页面
        dropDialog.show()
        dropDialog.exec_()

    def userManage(self):
        """
        用户删除管理
        """
        UserDelete = UserManage(self)
        UserDelete.show()
        UserDelete.exec_()


if __name__ == "__main__":
    """
    测试代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = AdminHome()
    mainWindow.show()
    sys.exit(app.exec_())
