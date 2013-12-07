#!/usr/bin/python
#coding=gbk
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.ui_mainwindow import *

class P2pMainWin( QMainWindow ):
	def __init__( self ):
		QMainWindow.__init__( self, parent=None )
		self.ui = Ui_MainWindow()
		self.ui.setupUi( self )
		self.createConnections()

	def openFiles( self ):
		print( 'You are trying to openFiles' )

	def createConnections( self ):
		self.connect( self.ui.fileOpenAction, SIGNAL('triggered()'),\
				self.openFiles )
	
	

import sys
app = QApplication( sys.argv )

myMainWin = P2pMainWin()
myMainWin.show()

sys.exit( app.exec_() )

