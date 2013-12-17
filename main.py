#!/usr/bin/python
#coding=utf-8
import json
import logging
import os
import socket
import struct
import sys
from filemanager import *
from getIp import *
from p2pconstants import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from peer import PeerInfo, AllPeerInfo
from recvseq import RecvSeq
from server import Server
from threading import Thread
from ui.ui_mainwindow import *
from peer import AllPeerInfo, PeerInfo
from p2pmainwin import P2pMainWin
from share.qrc_simpeP2p import *

reload( sys )
sys.setdefaultencoding('utf-8')
#codec='base64'
codec='utf-8'
def readConfigFile( fullpath ):
	pass

def setDownLoadDir():
	pass

def initLog():
	if not os.path.isdir( os.sep.join([config['appDataPath'],'data','log']) ):
		os.mkdir( os.sep.join([config['appDataPath'],'data','log']) )

	logging.basicConfig( filename=os.sep.join([config['appDataPath'],'data','log','p2p.log']),\
		level=logging.DEBUG, \
		format='%(asctime)-15s %(levelname)s:%(message)s' )
	logging.info( 'app start logging-------------------------------' )
	pass


def readConfigFile( fullpath ):
	pass

def createConfigFile( fullpath ):
	#todo test if exist config file
	f = open( fullpath+os.sep+'config', 'w' )
#todo replace \n with universal newlines
	f.writelines( '#DO NOT REMOVE THIS FILE\n' )
	f.writelines( '#不要删除这个文件!\n' )
	f.writelines( '#auto generated by the p2p app\n' )
	f.writelines( 'hashfile='+fullpath+os.sep+'data'+os.sep+'hashfile\n' )
	#todo
	f.close()
	pass

#winXP or win7/8
if 'nt' in os.name: 
	config['osprefix'] = '_'
else:
	config['osprefix'] = '.'
	pass
configFileFullPath = os.path.expanduser('~')+os.sep+config['osprefix']+'simpleP2p'
#todo
config['appDataPath'] = configFileFullPath
config['downloadPath'] = configFileFullPath+os.sep+'downloads'
config['hostname'] = getIp() 
config['port'] = 10087

'''
if os.path.isfile( configFileFullPath ):
	readConfigFile( configFileFullPath )
else:
	createConfigFile( configFileFullPath )
'''

def parseDataGet( obj, data, info ):
	'''
	this fxn analysis the data and reponse to it
	'''
	if 'type' not in data.keys():
		logging.error( str(data)+'\nhas no key "type"' )
		return ERR

	if data['type'] == 'GF':
		fileFullPath = os.sep.join([config['downloadPath'],data['filename']])
		if not os.path.isfile( fileFullPath ):
			dataSend = json.dumps( dict(type='NOF') )
			info[0].send( dataSend )
		else:
			f = open( fileFullPath,'rb' )
			iTtl = os.stat( fileFullPath ).st_size / (RECVBUFFSIZE/2)
			iCur = 0
			dataRead = f.read( RECVBUFFSIZE/2)
			while P2pMainWin.running and dataRead:
				dataSend = json.dumps(\
					dict(type='F',filename=data['filename'],seq=str(iCur)+' '+str(iTtl),data=dataRead.encode(codec) )\
					)
				print 'download data send '+str(iCur)
				if len(dataSend) < RECVBUFFSIZE:
					dataSend = dataSend + (RECVBUFFSIZE-len(dataSend))*' '
				info[0].send( dataSend )
				dataRead = f.read( RECVBUFFSIZE/2 )
				iCur = iCur + 1
			f.close()
		return ENDOFCONNECTION
#todo better way of if else
	if data['type'] == 'GFL':
		#todo get file list
#todo semaphore for file read here
		hashFilePath = os.sep.join( [config['appDataPath'],'data',\
				'hashfile'] ) 
		f = open( hashFilePath )
		iTtl = os.stat( hashFilePath ).st_size / (RECVBUFFSIZE/2)
		iCur = 0
		#minus 2048 for some other field such as type, and there will be many / added by json
		dataRead = f.read( RECVBUFFSIZE/2) 
		while P2pMainWin.running and dataRead:
			dataSend = json.dumps(\
					dict( type='FL', seq=str(iCur)+' '+str(iTtl),data=dataRead ) )
			if len( dataSend ) <= RECVBUFFSIZE:
				print str(len(dataSend))+' hashfile dataSend'
				dataSend = dataSend + (RECVBUFFSIZE-len(dataSend))*' '
			else:
				print 'error dataSend too large: '+str(len(dataSend))
				logging.error( 'dataSend '+str(len(dataSend))+' larger than'+\
					' buffersize '+str(RECVBUFFSIZE) )
			info[0].send( dataSend )
			dataRead = f.read( RECVBUFFSIZE/2)
			iCur = iCur + 1
		f.close()
		return  ENDOFCONNECTION
	
	if data['type'] == 'NOF':
		logging.info( 'parseDataGet get NOF from '+str(info[1]) )
		return ENDOFCONNECTION
	if data['type'] == 'F':
		#todo Oops! Some dup code with type=='FL'
		jar = RecvSeq.getJar( data['filename'] )
		jar.pushData( data )
		if jar.isfull:
			fBinData = jar.dataStr.decode(codec)
			#fBinData = jar.dataStr
			#print fBinData
			f = open( os.sep.join([config['downloadPath'],data['filename']]),'w')
			f.write( fBinData )
			f.close()
			'''
			P2pMainWin.appInstance.modallessMessageBox( data['filename']\
					+u' 下载完成' )
			'''
			print 'download end'
			logging.info( 'download file succeeded! '+str(len(fBinData))+' bytes' )
			RecvSeq.releaseJar( data['filename'] )
			return ENDOFCONNECTION

	if data['type'] == 'FL':
		jar = RecvSeq.getJar( info[1][1] )
		jar.pushData( data )
		if jar.isfull:
			p = AllPeerInfo.getPeer(info[1][0])
			p.fileDict = json.loads( jar.dataStr )

			netHashFilePath = os.sep.join( [config['appDataPath'],'data',\
					'nethashfile'] )
			f = open( netHashFilePath, 'w' )
			f.write( jar.dataStr )
			f.close()
			logging.info( 'nethashfile created!' )

			RecvSeq.releaseJar( info[1][1] )
			if P2pMainWin.appInstance:
				l = []
				for k,v in p.fileDict.iteritems():
					l.append( k )
				P2pMainWin.appInstance.setNetFileList( l )
			return ENDOFCONNECTION
		else:
			return 0

def createEssentialDir():
	if not os.path.isdir( config['appDataPath'] ):
		os.mkdir( config['appDataPath'] )
		os.mkdir( config['appDataPath']+os.sep+'data' )
		os.mkdir( os.sep.join( [config['appDataPath'],'data','log'] ) )
		createConfigFile( config['appDataPath'] )
	if not os.path.isdir( config['downloadPath'] ):
		os.mkdir( config['downloadPath'] )
	pass

#now start the application, build a qt app
app = QApplication( sys.argv )

createEssentialDir()
initLog()
Server.parseDataGet = parseDataGet
Server.serverd( (config['hostname'],config['port']) )

myMainWin = P2pMainWin()
P2pMainWin.appInstance = myMainWin
P2pMainWin.parseDataGet = parseDataGet
myMainWin.show()

FileMgr.downloadDirPath = config['downloadPath'] 
FileMgr.localHashFilePath = os.sep.join([config['appDataPath'],'data',\
		'hashfile'])
FileMgr.init()
AllPeerInfo.port = config['port']
AllPeerInfo.parseDataGet = parseDataGet
AllPeerInfo.getAllPeerFileList()

#todo close all thread
sys.exit( app.exec_() )
