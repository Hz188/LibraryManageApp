# -*- coding: utf-8 -*-
# addBookDialog.py
# @author 灏喆
# @description 添加图书
# @created 2019-05-25T12:25:14.324Z+08:00
# @last-modified 2019-06-13T12:46:26.771Z+08:00
#

import sys
import time

from PyQt5.Qt import *


class addBookDialog(QDialog):
    """
    添加书籍对话框
    """
    add_book_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addBookDialog, self).__init__(parent)
        self.setUpUI()
        # 设置窗口为窗口模态，程序在未处理完当前对话框时将阻止和对话框的父窗口进行交互
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("添加书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        BookCategory = [
            "数学", "计算机", "通信", "政治", "经济", "文化", "教育", "体育", "历史", "地理", "生物学",
            "医学", "农业"
        ]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件 显示文本
        self.titlelabel = QLabel("  添加书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")
        self.addNumLabel = QLabel("数    量:")

        # button控件
        self.addBookButton = QPushButton("添 加")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QDateTimeEdit()
        self.publishTime.setDisplayFormat("yyyy-MM-dd")
        self.addNumEdit = QLineEdit()

        self.bookNameEdit.setMaxLength(20)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)
        self.addNumEdit.setMaxLength(12)
        self.addNumEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow(self.addNumLabel, self.addNumEdit)
        self.layout.addRow("", self.addBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)
        self.addNumLabel.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookIdEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.publisherEdit.setFont(font)
        self.publishTime.setFont(font)
        self.categoryComboBox.setFont(font)
        self.addNumEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.addBookButton.setFont(font)
        self.addBookButton.setFixedHeight(32)
        self.addBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.addBookButton.clicked.connect(self.addBookButtonCicked)

    def addBookButtonCicked(self):
        """
        添加书籍逻辑
        """
        bookName = self.bookNameEdit.text()
        bookId = self.bookIdEdit.text()
        authName = self.authNameEdit.text()
        bookCategory = self.categoryComboBox.currentText()  # 返回选中的文本
        publisher = self.publisherEdit.text()
        publishTime = self.publishTime.text()
        addBookNum = self.addNumEdit.text()
        if ("" == bookName or "" == bookId or "" == authName
                or "" == bookCategory or "" == publisher or "" == publishTime
                or "" == addBookNum):
            QMessageBox.warning(self, "警告", "有字段为空，添加失败",
                                QMessageBox.Yes | QMessageBox.Yes)
            return
        else:
            addBookNum = int(addBookNum)
            db = QSqlDatabase.addDatabase("QMYSQL")
            db.setHostName("localhost")
            db.setPort(3306)
            db.setUserName("root")
            db.setPassword("123456")
            db.setDatabaseName("library")
            db.open()
            query = QSqlQuery()
            # 如果已存在，则update Book表的现存量，剩余可借量，不存在，则insert Book表，同时insert buyordrop表
            sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
            query.exec_(sql)
            if (query.next()):
                sql = "UPDATE Book SET NumStorage=NumStorage+%d,NumCanBorrow=NumCanBorrow+%d WHERE BookId='%s'" % (
                    addBookNum, addBookNum, bookId)
            else:
                sql = "INSERT INTO book VALUES ('%s','%s','%s','%s','%s','%s',%d,%d,0)" % (
                    bookName, bookId, authName, bookCategory, publisher,
                    publishTime, addBookNum, addBookNum)
            query.exec_(sql)
            db.commit()
            # 插入buyordrop表
            # 获取当前操作的时间，精度到天
            timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            sql = "INSERT INTO buyordrop VALUES ('%s','%s',1,%d)" % (
                bookId, timenow, addBookNum)
            query.exec_(sql)
            db.commit()
            QMessageBox.information(self, "提示", "添加书籍成功!",
                                    QMessageBox.Yes | QMessageBox.Yes)
            self.add_book_success_signal.emit()
            self.close()
            self.clearEdit()
        return

    def clearEdit(self):
        """
        插入结束后自动清空
        """
        self.bookNameEdit.clear()
        self.bookIdEdit.clear()
        self.authNameEdit.clear()
        self.addNumEdit.clear()
        self.publisherEdit.clear()


if __name__ == "__main__":
    """
    测试代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = addBookDialog()
    mainWindow.show()
    sys.exit(app.exec_())
