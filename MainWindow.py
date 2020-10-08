# -*- coding: utf-8 -*-
# MainWindow.py
# @author 灏喆
# @description 主窗口打开App
# @created 2019-05-25T17:03:50.436Z+08:00
# @last-modified 2019-06-13T11:10:41.110Z+08:00
#

import sys

from PyQt5.Qt import *
import sip

from SignIn import SignIn
from SignUp import SignUp
from AdminHome import AdminHome
from StudentHome import StudentHome
from changePasswordDialog import changePasswordDialog


class Main(QMainWindow):
    """主窗口"""

    def __init__(self, parent=None):
        """初始化UI"""
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignIn()
        self.resize(900, 600)
        self.setWindowTitle("欢迎登陆图书馆管理系统")
        self.setCentralWidget(self.widget)  # 初始页面
        bar = self.menuBar()  # 菜单栏
        self.Menu = bar.addMenu("菜单栏")
        self.signUpAction = QAction("注册", self)
        self.changePasswordAction = QAction("修改密码", self)
        self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.quitAction = QAction("退出", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        self.signUpAction.setEnabled(True)
        self.changePasswordAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)
        self.widget.is_admin_signal.connect(self.adminSignIn)
        self.widget.is_student_signal[str].connect(self.studentSignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)

    def adminSignIn(self):
        """管理员登陆"""
        sip.delete(self.widget)
        self.widget = AdminHome()
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)

    def studentSignIn(self, studentId):
        """学生用户登陆"""
        sip.delete(self.widget)
        self.widget = StudentHome(studentId)
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)

    def menuTriggered(self, q):
        """User行为"""
        if ("修改密码" == q.text()):
            changePsdDialog = changePasswordDialog(self)
            changePsdDialog.show()
            changePsdDialog.exec_()
        if ("注册" == q.text()):
            sip.delete(self.widget)
            self.widget = SignUp()
            self.setCentralWidget(self.widget)
            self.widget.student_signup_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
        if ("退出登录" == q.text()):
            sip.delete(self.widget)
            self.widget = SignIn()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if ("登录" == q.text()):
            sip.delete(self.widget)
            self.widget = SignIn()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if ("退出" == q.text()):
            QApplication.instance().quit()  # 获取当前App对象
        return


if __name__ == "__main__":
    """测试代码"""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    mainWindow = Main()
    mainWindow.show()
    sys.exit(app.exec_())
