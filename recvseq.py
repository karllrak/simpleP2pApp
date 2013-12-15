import time
import logging
from threading import Thread
class RecvSeq:
	'''RecvSeq is a class which get part of the received
	data( json parsed ), and paste them together
	'''
	portJar = {}
	gcInterval = 30

	@staticmethod
	def getJar( i ):
		if i in RecvSeq.portJar:
			return RecvSeq.portJar[i]
		else:
			RecvSeq.portJar[i] = RecvSeq()
			return RecvSeq.portJar[i]

	@staticmethod
	def releaseJar( i ):
		'''release jar by port number'''
		RecvSeq.portJar.pop( i )
		logging.info( str(i)+' recv jar released' )

	@staticmethod
	def fullJarCollecting():
		for key,v in RecvSeq.portJar.iteritems():
			if v.isfull:
				RecvSeq.portJar.pop( k )
		time.sleep( RecvSeq.gcInterval )	
		pass

	@staticmethod
	def init():
		'''start a new thread for garbage jar collecting'''
		#no need to gc, just mannually
		#t = Thread( target=RecvSeq.fullJarCollecting, args=() )
		#t.start()

	def __init__( self ):
		self.isfull = False
		self.dataStr = ''
		logging.info( 'recv jar created' )

	def pushData( self, data ):
		self.dataStr = self.dataStr + data['data']
		iCur, iTotal = data['seq'].split()
		if iCur == iTotal:
			self.isfull = True


