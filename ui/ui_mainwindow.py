# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Mon Dec 16 09:10:03 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(500, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 471, 421))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.searchLineEdit = QtGui.QLineEdit(self.widget)
        self.searchLineEdit.setObjectName(_fromUtf8("searchLineEdit"))
        self.gridLayout.addWidget(self.searchLineEdit, 1, 0, 1, 1)
        self.downloadBtn = QtGui.QPushButton(self.widget)
        self.downloadBtn.setObjectName(_fromUtf8("downloadBtn"))
        self.gridLayout.addWidget(self.downloadBtn, 1, 3, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.localFileListWidget = QtGui.QListWidget(self.widget)
        self.localFileListWidget.setObjectName(_fromUtf8("localFileListWidget"))
        self.gridLayout.addWidget(self.localFileListWidget, 3, 0, 1, 1)
        self.peerListWidget = QtGui.QListWidget(self.widget)
        self.peerListWidget.setObjectName(_fromUtf8("peerListWidget"))
        self.gridLayout.addWidget(self.peerListWidget, 3, 1, 1, 3)
        self.searchBtn = QtGui.QPushButton(self.widget)
        self.searchBtn.setObjectName(_fromUtf8("searchBtn"))
        self.gridLayout.addWidget(self.searchBtn, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.fileOpenAction = QtGui.QAction(MainWindow)
        self.fileOpenAction.setObjectName(_fromUtf8("fileOpenAction"))
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.menu.addAction(self.fileOpenAction)
        self.menu.addAction(self.exitAction)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.downloadBtn.setText(_translate("MainWindow", "下载(&download)", None))
        self.label.setText(_translate("MainWindow", "本地文件", None))
        self.label_2.setText(_translate("MainWindow", "伙伴", None))
        self.searchBtn.setText(_translate("MainWindow", "搜索(&search)", None))
        self.menu.setTitle(_translate("MainWindow", "文件", None))
        self.fileOpenAction.setText(_translate("MainWindow", "打开", None))
        self.fileOpenAction.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.exitAction.setText(_translate("MainWindow", "退出", None))
        self.exitAction.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

