# -*- coding: utf-8 -*-
# borrowBookDialog.py
# @author 灏喆
# @description 借书弹窗
# @created 2019-05-25T15:41:51.452Z+08:00
# @last-modified 2019-06-13T11:06:02.227Z+08:00
#

import sys
import time

from PyQt5.Qt import *


class borrowBookDialog(QDialog):
    """
    借书对话窗口
    """
    borrow_book_success_signal = pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(borrowBookDialog, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        # 设置窗口为窗口模态，程序在未处理完当前对话框时将阻止和对话框的父窗口进行交互
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("借阅书籍")

    def setUpUI(self):
        """
        UI界面
        """
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        BookCategory = [
            "数学", "计算机", "通信", "政治", "经济", "文化", "教育", "体育", "历史", "地理", "生物学",
            "医学", "农业"
        ]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.borrowStudentLabel = QLabel("借 阅 人:")
        self.borrowStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  借阅书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")

        # button控件
        self.borrowBookButton = QPushButton("确认借阅")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()

        self.bookNameEdit.setMaxLength(30)
        self.bookIdEdit.setMaxLength(6)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.borrowStudentLabel, self.borrowStudentIdLabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow("", self.borrowBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.borrowStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.borrowStudentLabel.setFont(font)
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
        self.borrowBookButton.setFont(font)
        self.borrowBookButton.setFixedHeight(32)
        self.borrowBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        # 信号
        self.borrowBookButton.clicked.connect(self.borrowButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)
        self.bookIdEdit.returnPressed.connect(self.borrowButtonClicked)

    def borrowButtonClicked(self):
        """
        借书内容正误逻辑判断
        """
        # 获取书号，书号为空或不存在库中，则弹出错误
        # 向Book_User表插入记录，更新User表以及Book表
        BookId = self.bookIdEdit.text()
        # BookId为空的处理
        if ("" == BookId):
            QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Yes,
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
        # 如果BookId不存在
        sql = "SELECT * FROM Book WHERE BookId='%s'" % BookId
        query.exec_(sql)
        # 执行成功则next依次取出 sql语句选择出来的每一行记录，若有数据则返回一个true
        if (not query.next()):
            QMessageBox.warning(self, "警告", "你所要借的书不存在，请查看输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            return

        # 借书上限5本
        sql = "SELECT COUNT(StudentId) FROM User_Book WHERE StudentId='%s' AND BorrowState=1" % (
            self.studentId)
        query.exec_(sql)
        if (query.next()):
            borrowNum = query.value(0)
            if (borrowNum == 5):
                QMessageBox.warning(self, "警告", "您借阅的书达到上限（5本）,借书失败！",
                                    QMessageBox.Yes, QMessageBox.Yes)
                return
        # 不允许重复借书
        sql = "SELECT COUNT(StudentId) FROM User_Book WHERE  StudentId='%s' AND BookId='%s' AND BorrowState=1" % (
            self.studentId, BookId)
        query.exec_(sql)
        if (query.next() and query.value(0)):
            QMessageBox.warning(self, "警告", "您已经借阅了本书并尚未归还，借阅失败！",
                                QMessageBox.Yes, QMessageBox.Yes)
            return
        # 更新User表
        sql = "UPDATE User SET TimesBorrowed=TimesBorrowed+1,NumBorrowed=NumBorrowed+1 WHERE StudentId='%s'" % self.studentId
        query.exec_(sql)
        db.commit()
        # 更新Book表
        sql = "UPDATE Book SET NumCanBorrow=NumCanBorrow-1,NumBorrowed=NumBorrowed+1 WHERE BookId='%s'" % BookId
        query.exec_(sql)
        db.commit()

        # 插入User_Book表
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "INSERT INTO User_Book VALUES ('%s','%s','%s',NULL,1)" % (
            self.studentId, BookId, timenow)
        query.exec_(sql)
        if not query.exec_(sql):
            print(1)
            query.exec_(
                "UPDATE User_Book set BorrowTime = '%s',ReturnTime = NUll, borrowstate = %d where BookId = '%s' and StudentId ='%s' "
                % (timenow, 1, BookId, self.studentId))
        db.commit()
        print(
            QMessageBox.information(self, "提示", "借阅成功!", QMessageBox.Yes,
                                    QMessageBox.Yes))
        self.borrow_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        """
        用户输入书号
        自动填充书籍信息
        """
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
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
        sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
        query.exec_(sql)
        # 查询对应书号，如果存在就更新form
        if (query.next()):
            self.bookNameEdit.setText(query.value(0))
            self.authNameEdit.setText(query.value(2))
            self.categoryComboBox.setCurrentText(query.value(3))
            self.publisherEdit.setText(query.value(4))
            self.publishTime.setText(query.value(5).toString(Qt.ISODate))
        return


if __name__ == "__main__":
    """
    测试代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = borrowBookDialog("2017210701")
    mainWindow.show()
    sys.exit(app.exec_())
