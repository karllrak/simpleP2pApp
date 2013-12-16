import socket
import logging
import json
from p2pconstants import RECVBUFFSIZE, ENDOFCONNECTION
from threading import Thread

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
		while Server.serverRunning:
			conSck, conAddr = s.accept()
			t = Thread( target=Server.serverAccept,args=((conSck,conAddr),) )
			t.start()
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
		while True:
			try:
				dataGet = conInfo[0].recv( RECVBUFFSIZE ) #todo warning too small buffer
			except socket.timeout:
				logging.info( 'connection to '+str(conInfo)+' timeout' )
				conInfo[0].close()
				break
			else:
				try:
					d = json.loads( dataGet )
				except ValueError:
					dataSend = json.dumps(\
						dict( type='ERR',data='Invalid format') )
					conInfo[0].send( dataSend )
					logging.error( 'json.loads  in serverAccept   meet ValueError from '+str(conInfo[1])+'\nwithdata:\n'+str(dataGet) )
				else:
					#dataGet can be json.loads  as d
					if Server.parseDataGet:
						if ENDOFCONNECTION == Server().parseDataGet(\
								d, conInfo ):
							conInfo[0].close()
							break
		pass
	

