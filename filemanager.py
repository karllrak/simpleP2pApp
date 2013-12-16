import json
import time
import os
import hashlib
import logging
from p2pconstants import *
from threading import Thread
from threading import BoundedSemaphore
#coding=utf-8
class FileInfo:
	def __init__( self, dirname=None, fname=None ):
		self.dirname = dirname
		self.fname = fname
		self.filesize = os.stat( os.sep.join([dirname,fname]) ).st_size
		self.hashArray = []
	def toDict( self ):
		return dict(dirname=self.dirname,fname=self.fname,\
				filesize=self.filesize,hashArray=self.hashArray)
	pass

class FileMgr:
	#local file hash in parts
	localFileDict = {}
	localHashFilePath = None
	syncInterval = 120
	downloadDirPath = None
	fileWriteSema = None
	fileBlockSize = 1024*64 
	@staticmethod
	def init():
		FileMgr.fileWriteSema = BoundedSemaphore( value=1 )
		t = Thread( target=FileMgr.syncd, args=() )
		t.start()
		pass
	@staticmethod
	def syncd():
		logging.info( 'sync daemon started' )
#todoi when to stop?
		i = 0
		from p2pmainwin import *
		while P2pMainWin.running:
			print str(P2pMainWin.running)+' syncd'
			if FileMgr.syncInterval == i:
				i = 0
				FileMgr.syncRoutine()
			else:
				i = i + 1
				time.sleep( 1 )
		print 'syncd exiting'
		pass
	@staticmethod
	def syncRoutine():
		if FileMgr.downloadDirPath:
			os.path.walk( FileMgr.downloadDirPath, FileMgr.createLocalHash, None )
		logging.info( 'syncRoutine once '+FileMgr.downloadDirPath )
		if FileMgr.localHashFilePath:
			#todoi lock here!
			FileMgr.fileWriteSema.acquire()
			try:
				f = open( FileMgr.localHashFilePath, 'w' )
			except IOError:
				logging.error( 'opening '+FileMgr.localHashFilePath+' meet IOError' )
				return
			else:
				f.write( json.dumps( FileMgr.localFileDict ) )
				f.close()
			FileMgr.fileWriteSema.release()
		pass
	@staticmethod
	def createLocalHash( arg, dirname, fnames ):
		for fname in fnames:
			#todo warning ! a list of file semaphore needed!
			fi = FileInfo(dirname,fname)

			f = open(os.sep.join([dirname,fname]),'r')
			dataRead = f.read( FileMgr.fileBlockSize )
			while P2pMainWin.running and dataRead:
				print P2pMainWin.running
				fi.hashArray.append( hashlib.sha1(dataRead).hexdigest())
				dataRead = f.read( FileMgr.fileBlockSize )
			f.close()
			#todo warning how can you save file in dict by fname?
			FileMgr.localFileDict[fname] = fi.toDict()
			

