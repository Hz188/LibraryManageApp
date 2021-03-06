# -*- coding: utf-8 -*-
# StudentHome.py
# @author 灏喆
# @description 学生主页
# @created 2019-05-25T13:09:17.954Z+08:00
# @last-modified 2019-06-13T10:28:25.648Z+08:00
#

import sys
import sip

from PyQt5.Qt import *

from BookStorageViewer import BookStorageViewer
from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog
from BorrowStatusViewer import BorrowStatusViewer


class StudentHome(QWidget):
    """
    主页
    """

    def __init__(self, studentId):
        super().__init__()
        self.StudentId = studentId
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        """
        UI界面
        """
        # 总布局
        self.layout = QHBoxLayout(self)
        # 按钮布局
        self.buttonLayout = QVBoxLayout()
        # 按钮
        self.borrowBookButton = QPushButton("借书")
        self.returnBookButton = QPushButton("还书")
        self.myBookStatus = QPushButton("借阅状态")
        self.allBookButton = QPushButton("所有书籍")
        self.buttonLayout.addWidget(self.borrowBookButton)
        self.buttonLayout.addWidget(self.returnBookButton)
        self.buttonLayout.addWidget(self.myBookStatus)
        self.buttonLayout.addWidget(self.allBookButton)
        self.borrowBookButton.setFixedWidth(100)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(100)
        self.returnBookButton.setFixedHeight(42)
        self.myBookStatus.setFixedWidth(100)
        self.myBookStatus.setFixedHeight(42)
        self.allBookButton.setFixedWidth(100)
        self.allBookButton.setFixedHeight(42)
        font = QFont()
        font.setPixelSize(16)
        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)
        self.myBookStatus.setFont(font)
        self.allBookButton.setFont(font)

        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.allBookButton.setEnabled(False)

        self.layout.addLayout(self.buttonLayout)
        self.layout.addWidget(self.storageView)

        self.borrowBookButton.clicked.connect(self.borrowBookButtonClicked)
        self.returnBookButton.clicked.connect(self.returnBookButtonClicked)
        self.myBookStatus.clicked.connect(self.myBookStatusClicked)
        self.allBookButton.clicked.connect(self.allBookButtonClicked)

    def borrowBookButtonClicked(self):
        """
        借书
        """
        borrowDialog = borrowBookDialog(self.StudentId, self)
        borrowDialog.borrow_book_success_signal.connect(
            self.borrowStatusView.borrowedQuery)
        borrowDialog.borrow_book_success_signal.connect(
            self.storageView.searchButtonClicked)
        borrowDialog.show()
        borrowDialog.exec_()
        return

    def returnBookButtonClicked(self):
        """
        还书
        """
        returnDialog = returnBookDialog(self.StudentId, self)
        returnDialog.return_book_success_signal.connect(
            self.borrowStatusView.returnedQuery)
        returnDialog.return_book_success_signal.connect(
            self.borrowStatusView.borrowedQuery)
        returnDialog.return_book_success_signal.connect(
            self.storageView.searchButtonClicked)
        returnDialog.show()
        returnDialog.exec_()

    def myBookStatusClicked(self):
        """
        图书借还状态记录
        """
        self.layout.removeWidget(self.storageView)
        sip.delete(self.storageView)
        self.storageView = BookStorageViewer()
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.layout.addWidget(self.borrowStatusView)
        self.allBookButton.setEnabled(True)
        self.myBookStatus.setEnabled(False)
        return

    def allBookButtonClicked(self):
        """
        图书信息
        """
        self.layout.removeWidget(self.borrowStatusView)
        sip.delete(self.borrowStatusView)
        self.borrowStatusView = BorrowStatusViewer(self.StudentId)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)
        self.allBookButton.setEnabled(False)
        self.myBookStatus.setEnabled(True)
        return


if __name__ == "__main__":
    """
    图书代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = StudentHome("2017210701")
    mainWindow.show()
    sys.exit(app.exec_())
