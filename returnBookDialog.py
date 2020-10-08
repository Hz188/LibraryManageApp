# -*- coding: utf-8 -*-
# returnBookDialog.py
# @author 灏喆
# @description 还书
# @created 2019-05-25T15:59:09.708Z+08:00
# @last-modified 2019-06-13T11:24:25.685Z+08:00
#

import sys
import time

from PyQt5.Qt import *


class returnBookDialog(QDialog):
    return_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(returnBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("归还书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        BookCategory = [
            "数学", "计算机", "通信", "政治", "经济", "文化", "教育", "体育", "历史", "地理", "生物学",
            "医学", "农业"
        ]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.returnStudentLabel = QLabel("还 书 人:")
        self.returnStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  归还书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")

        # button控件
        self.returnBookButton = QPushButton("确认归还")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.returnStudentLabel, self.returnStudentIdLabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow("", self.returnBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.returnStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.returnStudentLabel.setFont(font)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookNameEdit.setReadOnly(True)
        self.bookIdEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.authNameEdit.setReadOnly(True)
        self.publisherEdit.setFont(font)
        self.publisherEdit.setReadOnly(True)
        self.publishTime.setFont(font)
        self.categoryComboBox.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.returnBookButton.setFont(font)
        self.returnBookButton.setFixedHeight(32)
        self.returnBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.returnBookButton.clicked.connect(self.returnButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def returnButtonClicked(self):
        # 获取书号，书号为空或并未借阅，则弹出错误
        # 更新Book_User表User表以及Book表
        BookId = self.bookIdEdit.text()
        # BookId为空的处理
        if ("" == BookId):
            QMessageBox.warning(self, "警告", "你所要还的书不存在，请查看输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        # 打开数据库
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setPort(3306)
        db.setUserName("root")
        db.setPassword("123456")
        db.setDatabaseName("library")
        db.open()

        query = QSqlQuery()
        # 如果未借阅
        sql = "SELECT * FROM User_Book WHERE StudentId='%s' AND BookId='%s' AND BorrowState=1" % (
            self.studentId, BookId)
        query.exec_(sql)
        if (not query.next()):
            print(
                QMessageBox.information(self, "提示", "您并未借阅此书，故无需归还",
                                        QMessageBox.Yes, QMessageBox.Yes))
            return
        # 更新User表
        sql = "UPDATE User SET NumBorrowed=NumBorrowed-1 WHERE StudentId='%s'" % self.studentId
        query.exec_(sql)
        db.commit()
        # 更新Book表
        sql = "UPDATE Book SET NumCanBorrow=NumCanBorrow+1 WHERE BookId='%s'" % BookId
        query.exec_(sql)
        db.commit()
        # 更新User_Book表
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "UPDATE User_Book SET ReturnTime='%s',BorrowState=0 WHERE StudentId='%s' AND BookId='%s' AND BorrowState=1" % (
            timenow, self.studentId, BookId)
        query.exec_(sql)
        db.commit()
        print(
            QMessageBox.information(self, "提示", "归还成功!", QMessageBox.Yes,
                                    QMessageBox.Yes))
        self.return_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if ("" == bookId):
            self.bookNameEdit.clear()
            self.publisherEdit.clear()
            self.authNameEdit.clear()
            self.publishTime.clear()
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setPort(3306)
        db.setUserName("root")
        db.setPassword("123456")
        db.setDatabaseName("library")
        db.open()

        query = QSqlQuery()
        # 在User_Book表中找借阅记录，如果存在借阅，则更新form内容
        sql = "SELECT * FROM User_Book WHERE StudentId='%s' AND BookId='%s' AND BorrowState=1" % (
            self.studentId, bookId)
        query.exec_(sql)
        if (query.next()):
            # 更新form内容
            sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
            query.exec_(sql)
            # 查询对应书号，如果存在就更新form
            if (query.next()):
                self.bookNameEdit.setText(query.value(0))
                self.authNameEdit.setText(query.value(2))
                self.categoryComboBox.setCurrentText(query.value(3))
                self.publisherEdit.setText(query.value(4))
                # ISO格式日期打印
                self.publishTime.setText(query.value(5).toString(Qt.ISODate))
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = returnBookDialog("2017210701")
    mainWindow.show()
    sys.exit(app.exec_())
