# -*- coding: utf-8 -*-
# SignUp.py
# @author 灏喆
# @description 注册界面
# @created 2019-05-25T12:08:55.977Z+08:00
# @last-modified 2019-06-13T11:24:32.174Z+08:00
#

import sys
import hashlib

from PyQt5.Qt import *


class SignUp(QWidget):
    """
    登陆界面
    """
    # 注册成功信号，并传参
    student_signup_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        """
        UI界面
        """
        self.resize(900, 600)
        self.setWindowTitle("欢迎登陆图书管理系统")
        self.signUpLabel = QLabel(self)
        self.signUpLabel.setText("注册")
        self.signUpLabel.setAlignment(Qt.AlignCenter)  # 设置字体位置格式(居中)
        self.signUpLabel.setFixedHeight(100)

        font = QFont()
        font.setPixelSize(36)  #字体设置36pix
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.signUpLabel.setFont(font)

        self.layout = QVBoxLayout()  # 垂直布局，便于让各种控件再Widget控件中居中
        self.layout.addWidget(self.signUpLabel, Qt.AlignCenter)  # 设置居中
        self.setLayout(self.layout)  # 顶层空间加入布局

        # 表单布局  学号 姓名 密码 确认密码 标签以及对应单行输入文本
        self.formLayout = QFormLayout()
        self.formLayout.setAlignment(Qt.AlignRight)
        font.setPixelSize(18)

        # 1.第一行 学号 ： 输入栏
        # 1.1标签
        self.studentIdLabel = QLabel()
        self.studentIdLabel.setText("学号：")
        self.studentIdLabel.setFont(font)
        self.studentIdLabel.setAutoFillBackground(True)
        # 1.2输入栏
        self.studentIdLineEdit = QLineEdit()
        self.studentIdLineEdit.setFixedWidth(180)
        self.studentIdLineEdit.setFixedHeight(32)
        self.studentIdLineEdit.setFont(lineEditFont)
        self.studentIdLineEdit.setMaxLength(10)  # 最大输入长度 下同
        # 1.3添加至表单
        self.formLayout.addRow(self.studentIdLabel, self.studentIdLineEdit)

        # 2.第二行 姓名：输入栏
        # 2.1标签
        self.studentNameLabel = QLabel()
        self.studentNameLabel.setText("姓名：")
        self.studentNameLabel.setFont(font)
        # 2.2输入栏
        self.studentNameLineEdit = QLineEdit()
        self.studentNameLineEdit.setFixedWidth(180)
        self.studentNameLineEdit.setFixedHeight(32)
        self.studentNameLineEdit.setFont(lineEditFont)
        self.studentNameLineEdit.setMaxLength(10)
        # 2.3添加至表单
        self.formLayout.addRow(self.studentNameLabel, self.studentNameLineEdit)

        # 3.第三行 密码：输入栏
        # 3.1标签
        self.passwordLabel = QLabel()
        self.passwordLabel.setText("密码：")
        self.passwordLabel.setFont(font)
        # 3.2输入栏
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setMaxLength(10)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)  # 设置单行文本显示模式
        # 3，3添加至表单
        self.formLayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # 第四行  确认密码
        # 4.1标签
        self.passwordConfirmLabel = QLabel()
        self.passwordConfirmLabel.setText("确认密码:")
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLabel.setAlignment(Qt.AlignRight)
        # 3.2输入栏
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        self.passwordConfirmLineEdit.setMaxLength(10)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        # 4.3添加至表单
        self.formLayout.addRow(self.passwordConfirmLabel,
                               self.passwordConfirmLineEdit)

        # 最后 注册确认按钮
        self.signUpButton = QPushButton()
        self.signUpButton.setText("注册")
        self.signUpButton.setFixedHeight(30)
        self.signUpButton.setFixedWidth(120)
        self.signUpButton.setFont(font)
        self.formLayout.addRow("", self.signUpButton)

        widget1 = QWidget()
        widget1.setLayout(self.formLayout)
        widget1.setFixedHeight(250)
        widget1.setFixedWidth(300)

        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget1, Qt.AlignCenter)

        widget2 = QWidget()
        widget2.setLayout(self.Hlayout)
        self.layout.addWidget(widget2, Qt.AlignHCenter)
        widget2.show()

        # 设置验证器进行格式验证 利用正则表达式匹配用户输入内容是否符合规范，非常方便，学到了
        regId = QRegExp("[0-9]{10}")  # 可输入学号为10位0-9数字
        pValidator1 = QRegExpValidator(self)
        pValidator1.setRegExp(regId)
        self.studentIdLineEdit.setValidator(pValidator1)

        regPassword = QRegExp("[0-9A-Za-z]+$")  # 可输入密码可以有字母和数字 区分大小写
        pValidator2 = QRegExpValidator(self)
        pValidator2.setRegExp(regPassword)
        self.passwordLineEdit.setValidator(pValidator2)

        # 信号与槽建立连接 反馈用户行为
        self.signUpButton.clicked.connect(self.SignUp)
        # 回车被按下也触发槽函数
        self.studentIdLineEdit.returnPressed.connect(self.SignUp)
        self.studentNameLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        """
        注册逻辑判定
        """
        # 获取用户输入内容
        studentId = self.studentIdLineEdit.text()
        studentName = self.studentNameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.passwordConfirmLineEdit.text()
        if ("" == studentId or "" == studentName or "" == password
                or "" == confirmPassword):
            QMessageBox.warning(self, "警告", "表单不可为空，请重新输入", QMessageBox.Yes,
                                QMessageBox.Yes)

            return
        else:  # 需要处理逻辑，1.账号已存在;2.密码没两遍输对;3.注册成功插入user表
            db = QSqlDatabase.addDatabase("QMYSQL")
            db.setHostName("localhost")
            db.setPort(3306)
            db.setUserName("root")
            db.setPassword("123456")
            db.setDatabaseName("library")
            db.open()
            query = QSqlQuery()
            if (confirmPassword != password):
                QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入",
                                    QMessageBox.Yes, QMessageBox.Yes)
                return
            elif (confirmPassword == password):
                # md5编码
                hl = hashlib.md5()
                hl.update(password.encode(encoding='utf-8'))
                md5password = hl.hexdigest()
                sql = "SELECT * FROM user WHERE StudentId='%s'" % (studentId)
                query.exec_(sql)
                if (query.next()):
                    QMessageBox.warning(self, "警告", "该账号已存在,请重新输入",
                                        QMessageBox.Yes, QMessageBox.Yes)
                    return
                else:
                    sql = "INSERT INTO user VALUES ('%s','%s','%s',0,0,0)" % (
                        studentId, studentName, md5password)
                    db.exec_(sql)
                    db.commit()
                    QMessageBox.information(self, "提醒", "您已成功注册账号!",
                                            QMessageBox.Yes, QMessageBox.Yes)
                    self.student_signup_signal.emit(studentId)
                db.close()
                return


if __name__ == "__main__":
    """
    测试代码
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = SignUp()
    mainWindow.show()
    sys.exit(app.exec_())
