# -*- coding: utf-8 -*-
# SignIn.py
# @author 灏喆
# @description 登陆界面
# @created 2019-05-25T12:15:23.310Z+08:00
# @last-modified 2019-06-13T11:24:27.060Z+08:00
#

import sys
import hashlib

from PyQt5.Qt import *


class SignIn(QWidget):
    is_admin_signal = pyqtSignal()
    is_student_signal = pyqtSignal(str)

    def __init__(self):
        super(SignIn, self).__init__()
        self.resize(900, 600)
        self.setWindowTitle("欢迎使用图书馆管理系统")
        self.setUpUI()

    def setUpUI(self):
        """
        UI界面
        """
        # 层次控件
        self.Vlayout = QVBoxLayout(self)
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()
        self.formlayout = QFormLayout()

        # 非抽象控件
        self.label1 = QLabel("学号: ")
        labelFont = QFont()
        labelFont.setPixelSize(18)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.label1.setFont(labelFont)
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setFixedHeight(32)
        self.lineEdit1.setFixedWidth(180)
        self.lineEdit1.setFont(lineEditFont)
        self.lineEdit1.setMaxLength(10)
        self.formlayout.addRow(self.label1, self.lineEdit1)

        self.label2 = QLabel("密码: ")
        self.label2.setFont(labelFont)
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setFixedHeight(32)
        self.lineEdit2.setFixedWidth(180)
        self.lineEdit2.setMaxLength(16)
        self.formlayout.addRow(self.label2, self.lineEdit2)

        # 设置验证
        reg = QRegExp("[0~9]{10}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEdit1.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEdit2.setValidator(pValidator)

        passwordFont = QFont()
        passwordFont.setPixelSize(10)
        self.lineEdit2.setFont(passwordFont)

        self.lineEdit2.setEchoMode(QLineEdit.Password)
        self.signIn = QPushButton("登 录")
        self.signIn.setFixedWidth(80)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)
        self.formlayout.addRow("", self.signIn)

        self.label = QLabel("欢迎使用图书馆管理系统")
        fontlabel = QFont()
        fontlabel.setPixelSize(30)
        self.label.setFixedWidth(390)
        self.label.setFont(fontlabel)
        self.Hlayout1.addWidget(self.label, Qt.AlignCenter)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.Hlayout1)
        self.widget2 = QWidget()
        self.widget2.setFixedWidth(300)
        self.widget2.setFixedHeight(150)
        self.widget2.setLayout(self.formlayout)
        self.Hlayout2.addWidget(self.widget2, Qt.AlignCenter)
        self.widget = QWidget()
        self.widget.setLayout(self.Hlayout2)
        self.Vlayout.addWidget(self.widget1)
        self.Vlayout.addWidget(self.widget, Qt.AlignTop)

        self.signIn.clicked.connect(self.signInCheck)
        self.lineEdit2.returnPressed.connect(self.signInCheck)
        self.lineEdit1.returnPressed.connect(self.signInCheck)

    def signInCheck(self):
        """
        登陆逻辑判定
        """
        studentId = self.lineEdit1.text()
        password = self.lineEdit2.text()
        if ("" == studentId or "" == password):
            QMessageBox.warning(self, "警告", "学号和密码不可为空!", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        # 打开数据库连接
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setPort(3306)
        db.setUserName("root")
        db.setPassword("123456")
        db.setDatabaseName("library")
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM user WHERE StudentId='%s'" % (studentId)
        query.exec_(sql)
        db.close()

        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        if (not query.next()):
            QMessageBox.information(self, "提示", "该账号不存在!", QMessageBox.Yes,
                                    QMessageBox.Yes)
        else:
            if (studentId == query.value(0)
                    and hl.hexdigest() == query.value(2)):
                # 如果是管理员 或普通用户
                if (1 == query.value(3)):
                    self.is_admin_signal.emit()
                else:
                    self.is_student_signal.emit(studentId)
            else:
                QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes,
                                        QMessageBox.Yes)
        return


if __name__ == "__main__":
    """
    测试函数
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = SignIn()
    mainWindow.show()
    sys.exit(app.exec_())
