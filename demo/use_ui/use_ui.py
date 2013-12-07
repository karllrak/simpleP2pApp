#!/usr/bin/python
#coding=gbk

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui27test import * #这是从ui文件里面产生的
import sys

app = QApplication( sys.argv )

ui_win = Ui_MainWindow()
mainWin = QMainWindow()
ui_win.setupUi( mainWin )
mainWin.show()

sys.exit( app.exec_() )


