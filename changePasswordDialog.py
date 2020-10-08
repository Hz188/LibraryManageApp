# -*- coding: utf-8 -*-
# changePasswordDialog.py
# @author 灏喆
# @description 修改密码
# @created 2019-05-25T16:01:05.533Z+08:00
# @last-modified 2019-06-13T11:07:14.509Z+08:00
#

import sys
import time
import hashlib

from PyQt5.Qt import *


class changePasswordDialog(QDialog):
    """
    用户修改代码对话窗口
    """

    def __init__(self, parent=None):
        super(changePasswordDialog, self).__init__(parent)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("修改密码")
        self.setUpUI()

    def setUpUI(self):
        """
        UI界面
        """
        self.resize(300, 280)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.titlelabel = QLabel(" 修改密码")

        self.studentIdLabel = QLabel("学    号：")
        self.oldPasswordLabel = QLabel("旧 密 码：")
        self.passwordLabel = QLabel("新 密 码：")
        self.confirmPasswordLabel = QLabel("确认密码：")

        self.studentIdEdit = QLineEdit()
        self.oldPasswordEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.confirmPasswordEdit = QLineEdit()

        self.changePasswordButton = QPushButton("确认修改")
        self.changePasswordButton.setFixedWidth(140)
        self.changePasswordButton.setFixedHeight(32)

        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.studentIdLabel, self.studentIdEdit)
        self.layout.addRow(self.oldPasswordLabel, self.oldPasswordEdit)
        self.layout.addRow(self.passwordLabel, self.passwordEdit)
        self.layout.addRow(self.confirmPasswordLabel, self.confirmPasswordEdit)
        self.layout.addRow("", self.changePasswordButton)

        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.studentIdLabel.setFont(font)
        self.oldPasswordLabel.setFont(font)
        self.passwordLabel.setFont(font)
        self.confirmPasswordLabel.setFont(font)

        font.setPixelSize(16)
        self.studentIdEdit.setFont(font)
        self.changePasswordButton.setFont(font)
        font.setPixelSize(10)
        self.oldPasswordEdit.setFont(font)
        self.passwordEdit.setFont(font)
        self.confirmPasswordEdit.setFont(font)

        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        # 设置长度
        self.studentIdEdit.setMaxLength(10)
        self.oldPasswordEdit.setMaxLength(16)
        self.passwordEdit.setMaxLength(16)
        self.confirmPasswordEdit.setMaxLength(16)
        # 设置密码模式
        self.oldPasswordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.confirmPasswordEdit.setEchoMode(QLineEdit.Password)

        # 设置校验器
        reg = QRegExp("[0~9]{10}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.studentIdEdit.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.oldPasswordEdit.setValidator(pValidator)
        self.passwordEdit.setValidator(pValidator)
        self.confirmPasswordEdit.setValidator(pValidator)

        # 设置信号与槽
        self.changePasswordButton.clicked.connect(
            self.changePasswordButtonClicked)

    def changePasswordButtonClicked(self):
        """
        修改密码逻辑实现，以及异常检测
        """
        studentId = self.studentIdEdit.text()
        oldPassword = self.oldPasswordEdit.text()
        password = self.passwordEdit.text()
        confirmPassword = self.confirmPasswordEdit.text()
        if ("" == studentId or "" == oldPassword or "" == password
                or "" == confirmPassword):
            QMessageBox.warning(self, "警告", "输入不可为空，请重新输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            return
        db = QSqlDatabase.addDatabase("QMYSQL")
        db.setHostName("localhost")
        db.setPort(3306)
        db.setUserName("root")
        db.setPassword("123456")
        db.setDatabaseName("library")
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM User WHERE StudentId='%s'" % studentId
        query.exec_(sql)
        # 如果用户不存在
        if (not query.next()):
            QMessageBox.warning(self, "警告", "该用户不存在，请重新输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            self.studentIdEdit.clear()
            return
            # 如果密码错误
        hl = hashlib.md5()
        hl.update(oldPassword.encode(encoding='utf-8'))
        md5password = hl.hexdigest()
        sql = "SELECT * FROM User WHERE Password='%s' AND StudentId='%s'" % (
            md5password, studentId)
        query.exec_(sql)
        if (not query.next()):
            QMessageBox.warning(self, "警告", "原密码输入错误,请重新输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            self.oldPasswordEdit.clear()
            return
        # 密码与确认密码不同
        if (password != confirmPassword):
            QMessageBox.warning(self, "警告", "两次输入密码不同,请确认输入", QMessageBox.Yes,
                                QMessageBox.Yes)
            self.passwordEdit.clear()
            self.confirmPasswordEdit.clear()
            return
        # 修改密码
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        md5password = hl.hexdigest()
        sql = "UPDATE User SET Password='%s' WHERE StudentId='%s'" % (
            md5password, studentId)
        query.exec_(sql)
        db.commit()
        QMessageBox.information(self, "提醒", "修改密码成功，请登录系统!", QMessageBox.Yes,
                                QMessageBox.Yes)
        self.close()
        return


if __name__ == "__main__":
    """
    测试代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = changePasswordDialog()
    mainWindow.show()
    sys.exit(app.exec_())
