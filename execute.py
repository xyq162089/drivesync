#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
程序做守护进程，轮训检查挂载目录，
当发现新挂载文件时候，开启同步目录下指定扩展名的文件
配合相册应用 PhotoPrism 实现相册功能
'''
import os, sys
import json
import logging
import time
import psutil
import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from imgsync import ImgSync
from db import databaseRequest
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMenu, QAction, qApp, QApplication, QMainWindow, QSystemTrayIcon, QDesktopWidget
from ui.main import Ui_mainWindow


class MyWindow(QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.tray = TrayIcon(self)
        self.setupUi(self)
        self.setWindowTitle("相册同步工具")
        self.setWindowIconText("相册同步工具")
        self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
        self.thread = Worker()
        self.thread.detail.connect(self.updateStatusDetail)
        self.thread.label.connect(self.updateStatusLabel)
        self.cleanButton.clicked.connect(self.cleanButtonClicked)
        self.thread.start()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray.show()

    def cleanButtonClicked(self):
        self.statusDetail.setText("")

    def updateStatusDetail(self, text):
        self.statusDetail.append(text)  # 文本框逐条添加数据
        self.statusDetail.moveCursor(self.statusDetail.textCursor().End)  # 文本框显示到底部

    def updateStatusLabel(self, text):
        self.statusLabel.setText(text)


class TrayIcon(QSystemTrayIcon):
    def __init__(self, MainWindow, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.ui = MainWindow
        self.createMenu()

    def createMenu(self):
        self.menu = QMenu()
        self.showAction = QAction("打开", self, triggered=self.show_window)
        self.quitAction = QAction("退出", self, triggered=self.quit)

        self.menu.addAction(self.showAction)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

        # 设置图标
        self.setIcon(QtGui.QIcon("./icon.jpg"))
        self.icon = self.MessageIcon()

        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    def quit(self):
        qApp.quit()

    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
    def onIconClicked(self, reason):
        if reason == 3:
            desktop = QDesktopWidget().availableGeometry()
            print(desktop.right(), desktop.topLeft())

            self.ui.move(desktop.right()-550, 11)
            self.ui.showNormal()
            self.ui.activateWindow()
            self.ui.setWindowFlags(Qt.Window)
            self.ui.show()
            self.hide()

        if reason == 2:
            if self.ui.isMinimized() or not self.ui.isVisible():
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                self.ui.showNormal()
                self.ui.activateWindow()
                self.ui.setWindowFlags(Qt.Window)
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()
                self.ui.setWindowFlags(Qt.SplashScreen)
                self.ui.show()


class Worker(QThread):
    detail = pyqtSignal(str)
    label = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)

    def run(self):

        logging.basicConfig(level=logging.ERROR)
        with open('config.json') as f:
            config = json.load(f)
        db = databaseRequest(config['database_path'])
        config['to_path'] = time.strftime('%Y-%m-%d')
        if not os.path.isdir(config['to_path']):
            os.makedirs(config['to_path'])

        processes = 1
        if multiprocessing.cpu_count() > 2:
            processes = multiprocessing.cpu_count() - 1

        # execute.ExecuteSync('/Users/wangxi/work/python/imgSync/ddadsf')
        baseDiskinfo = psutil.disk_partitions()

        pool = ThreadPool(processes=processes)
        execute = ImgSync(pool=pool, database=db, detailshow=self.detail, toPath=config['to_path'],
                          syncExt=['.jpg', '.jpeg', '.png', '.gif'])
        while True:
            diskInfo = psutil.disk_partitions()
            for disk in diskInfo:
                if disk not in baseDiskinfo:
                    self.label.emit("开始同步" + disk.mountpoint)
                    print("开始同步--")
                    execute.ExecuteSync(disk.mountpoint)
                    baseDiskinfo.append(disk)
                    self.label.emit("同步完成" + disk.mountpoint)

            # 拔出检测
            for i in baseDiskinfo:
                if i not in diskInfo:
                    baseDiskinfo.remove(i)
            time.sleep(5)

        pool.close()
        pool.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    tray = TrayIcon(myWin)
    # myWin.show()
    tray.show()
    sys.exit(app.exec_())
