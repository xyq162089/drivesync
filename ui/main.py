# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setEnabled(True)
        mainWindow.resize(300, 180)
        mainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(10, 10, 61, 18))
        self.title.setObjectName("title")
        self.statusDetail = QtWidgets.QTextBrowser(self.centralwidget)
        self.statusDetail.setGeometry(QtCore.QRect(10, 40, 271, 61))
        self.statusDetail.setObjectName("statusDetail")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(80, 10, 211, 21))
        self.statusLabel.setObjectName("statusLabel")
        self.cleanButton = QtWidgets.QToolButton(self.centralwidget)
        self.cleanButton.setGeometry(QtCore.QRect(10, 110, 130, 20))
        self.cleanButton.setObjectName("cleanButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.title.setText(_translate("mainWindow", "相册同步:"))
        self.statusLabel.setText(_translate("mainWindow", "无U盘插入"))
        self.cleanButton.setText(_translate("mainWindow", "清空"))
