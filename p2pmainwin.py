#!/usr/bin/python
#coding=utf-8
import logging
import json
import socket
import sys
from p2pconstants import *
from threading import Thread
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from peer import *
from ui.ui_mainwindow import *

class P2pMainWin( QMainWindow ):
	appInstance = None
	running = True
	parseDataGet = None
	def __init__( self ):
		QMainWindow.__init__( self, parent=None )
		self.ui = Ui_MainWindow()
		self.ui.setupUi( self )
		self.isquiting = False
		self.ui.ipListForFilename = QListWidget()
		self.systemTray = QSystemTrayIcon( self )
		self.systemTrayMenu = QMenu( self )
		self.windowIcon = QIcon(u':/share/systemTray.png')
		self.trayIcon = QIcon(u':/share/ef.ico')
		self.setWindowIcon( self.windowIcon )

		self.act_restore = QAction( u"恢复窗口", self );
		self.act_exit = QAction( u"退出" ,self );
		self.systemTrayMenu.addAction( self.act_restore );
		self.systemTrayMenu.addSeparator();
		self.systemTrayMenu.addAction( self.act_exit );

		self.systemTray.setContextMenu( self.systemTrayMenu )
		self.systemTray.setIcon( self.trayIcon )
		self.systemTray.show()
		self.systemTray.showMessage( 'simpleP2p', u'后台运行中...' )
		self.createConnections()
		self.setFixedSize(500,500)
		from peer import *
		for peer in AllPeerInfo.goodPeerIpList:
			self.ui.peerListWidget.addItem( peer )

	def showIpListForFile( self, fname, ipList ):
		self.ui.ipListForFilename.setWindowTitle( fname )
		self.ui.ipListForFilename.clear()
		for ip in ipList:
			self.ui.ipListForFilename.addItem( ip )
		#self.ui.ipListForFilename.setModal( False )
		#self.ui.ipListForFilename.show()
		self.emit(SIGNAL('showList'))

	def showList( self ):
		self.ui.ipListForFilename.show()
	def modallessMessageBox( self,text ):
		mb = QMessageBox()
		mb.setText( text )
		mb.setModal( False )
		mb.show()

	def closeEvent( self, evt ):
		if self.isquiting:
			P2pMainWin.running = False
			global P2PRUNNING
			P2PRUNNING = False
			print 'Goodbye!'
			logging.info( 'app exit ++++++++++++++' )
			evt.accept()
			sys.exit()
		else:
			self.hide()
			evt.ignore()

	def setNetFileList( self, l ):
		for item in l:
			self.ui.localFileListWidget.addItem( item )

	def downloadFile( self ):
		selectedList = self.ui.localFileListWidget.selectedItems()
		if 0 == len(selectedList):
			QMessageBox.information(None,'Error',u'没有选择任何文件')
		else:
			logging.info( 'download file begin' )
			#a list a filename to be download, actually there is only one
			filenameList = [str(i.text()) for i in selectedList]
			statusBar = self.statusBar()
			statusBar.showMessage( u'下载文件'+filenameList[0]+u'中...', 4 )
			print u'downloading file... '+str(filenameList)
			downloadThread( filenameList )

	def openFiles( self ):
		print( 'You are trying to openFiles' )
	def searchFile( self ):
		filename = self.ui.searchLineEdit.text()
		logging.info( u'search for file '+filename )
		statusBar = self.statusBar()
		statusBar.showMessage( u'搜索文件'+filename+u'中', 3 )
		print u'searching file '+filename
	def exit( self ):
		P2pMainWin.running = False
		self.isquiting = True
		sys.exit()

	def createConnections( self ):
		self.connect( self.ui.fileOpenAction, SIGNAL('triggered()'),\
				self.openFiles )
		self.connect( self.ui.downloadBtn, SIGNAL('clicked()'),\
				self.downloadFile )
		self.connect( self.ui.searchBtn, SIGNAL('clicked()'),\
				self.searchFile )
		self.connect( self,SIGNAL('showList'),self.showList )
		self.connect( self.act_exit,SIGNAL('triggered()'), self.exit )
		self.connect( self.act_restore, SIGNAL('triggered()'),self.showNormal )
		self.connect( self.ui.exitAction, SIGNAL('triggered()'),\
				self.exit )
	pass

def downloadThread( flist ):
	for f in flist:
		t = Thread( target=downloadFile, args=(f,) )
		t.start()
		ip = AllPeerInfo.getIpListByFilename( f )
		P2pMainWin.appInstance.showIpListForFile( f, ip )
def downloadFile( filename ):
	#todo download file from multi ip
	ip = AllPeerInfo.getIpListByFilename( filename )
	#todo else?
	if ip:
		#todoi duplicate codes with peer.py line 52
		#can use a class Name request blablabla
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.connect( (ip[0], config['port']) )
		logging.info( 'downloadFile connected to '+ip[0]+' '+str(config['port']) )
		#todo extend the fields	
		dataSend = json.dumps( dict(type='GF',filename=filename) )
		s.send( dataSend )
		s.settimeout( 500 )
		while P2pMainWin.running:
			try:
				dataGet = s.recv( RECVBUFFSIZE )
			except socket.timeout:
				logging.info( 'time out when downloadFile( %s )', ip[0] )
				s.close()
				break
			else:
				try:
					dataGet = json.loads( dataGet )
				except ValueError as ve:
					print 'downloadFile json.loads meet ValueError:'\
							+ve.message+' with data\n'+str( dataGet )
					s.close()
					break
				if ENDOFCONNECTION == AllPeerInfo().parseDataGet(dataGet,(s,(ip[0],config['port'])) ):
					s.close()
					break
			pass
		s.close()

