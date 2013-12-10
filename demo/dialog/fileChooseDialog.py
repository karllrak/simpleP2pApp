#coding=utf-8
from os.path import expanduser
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyDialog( QDialog ):
	def __init__( self ):
		QDialog.__init__( self, parent=None )
		gridLayout = QGridLayout()
		gridLayout.addWidget( QLabel( 'Choose a directory...'),
				0,0, Qt.AlignLeft )
		gridLayout.addWidget( QLineEdit( expanduser('~') ),
				1,0, Qt.AlignLeft )
		self.fileChooseBtn = QPushButton( 'More..')
		gridLayout.addWidget( self.fileChooseBtn,
				1,1, Qt.AlignRight )
		self.setLayout( gridLayout )
		self.connect( self.fileChooseBtn, SIGNAL('clicked()'),self.chooseFile )
	def chooseFile( self ):
		print 'You are choosing file!'
		fileDlg = QFileDialog( self )
		fileDlg.setFileMode( QFileDialog.DirectoryOnly )
		if fileDlg.exec_():
			filesSelected = fileDlg.selectedFiles()
			print filesSelected


	def keyPressEvent( self, e ):
		if e.key() == Qt.Key_Escape:
			print 'Use Enter Please!'
			return
		print str(e.key())+' is pressed'
#下面这个貌似没有用,捕捉不到回车
		if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
			print 'click the x to close'
	pass

import sys
app = QApplication( sys.argv )
mydlg = MyDialog()
mydlg.exec_()



