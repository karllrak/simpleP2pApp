#coding=utf-8
import socket
import logging
import json
from p2pconstants import *
from threading import Thread
from p2pmainwin import *

class Server:
	serverRunning = True
	parseDataGet = None
	@staticmethod
	def serverd( localhostInfo ):
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) 
		s.bind( localhostInfo )
		s.listen( 1 )
		t = Thread( target=Server.serverRoutine,args=(s,) )
		t.start()

	@staticmethod
	def serverRoutine( s ):
		logging.info( 'server start listening' )
		s.settimeout(0.5)
		while P2pMainWin.running and Server.serverRunning:
			try:
				conSck, conAddr = s.accept()
			except socket.timeout:
				continue
			else:
				t = Thread( target=Server.serverAccept,args=((conSck,conAddr),) )
				t.start()
			#print P2pMainWin.running
		print 'serverRunning ended'
		pass

	@staticmethod
	def serverAccept( conInfo ):
		'''
		this fxn most of the time is in a new thread and the 
		fxn itself must close the socket
		@params
		conInfo: tuple (conSock,conAddr)
		@return
		return nothing
		'''
		logging.info( 'serverAccept connected to '+str(conInfo[1]) )
		conInfo[0].settimeout( 2 )
		while P2pMainWin.running:
			try:
				dataGet = conInfo[0].recv( RECVBUFFSIZE ) #todo warning too small buffer
			except socket.timeout:
				logging.info( 'connection to '+str(conInfo)+' timeout' )
				conInfo[0].close()
				break
			else:
				try:
					d = json.loads( dataGet )
				except ValueError as ve:
					dataSend = json.dumps(\
						dict( type='ERR',data='Invalid format') )
					conInfo[0].send( dataSend )
					print 'serverAccept json.loads  meet ValueError: '+\
							ve.message+' with data\n'+str(dataGet)
					logging.error( 'json.loads  in serverAccept   meet ValueError from '+str(conInfo[1])+'\nwithdata:\n'+str(dataGet) )
				else:
					#dataGet can be json.loads  as d
					if Server.parseDataGet:
						if ENDOFCONNECTION == Server().parseDataGet(\
								d, conInfo ):
							conInfo[0].close()
							break
		print 'serverAccept ended ' + str(conInfo[1])
		conInfo[0].close()
		pass
	

