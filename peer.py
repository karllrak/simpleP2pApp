import logging
import socket
import json
from p2pconstants import *
from threading import Thread

class PeerInfo:
	#todo nickname for peer
	def __init__( self, ip=None ):
		self.ip = ip
		self.fileDict = None
		if ip:
			logging.info( 'peer with ip '+ip+' created' )
	pass

class AllPeerInfo:
	#peerList = ['10.0.2.15',]
	port = 10087
	#goodPeerIpList = ['10.0.2.15','10.22.142.138']
	goodPeerIpList = ['10.22.142.138']
	peerList = {}
	parseDataGet = None
	@staticmethod
	def getPeer( ip ):
		if ip in AllPeerInfo.peerList:
			return AllPeerInfo.peerList[ip];
		else:
			AllPeerInfo.peerList[ip] = PeerInfo()
			return AllPeerInfo.peerList[ip]
	@staticmethod
	def findPeers():
		return AllPeerInfo.peerList
	pass

	@staticmethod
	def getAllPeerFileList():
	#todoI get the peer list
		#for ip,info  in AllPeerInfo.peerList:
		for ip in AllPeerInfo.goodPeerIpList:
			t = Thread( target=AllPeerInfo.getOnePeerFileList, args=(ip,) )
			t.start()
		pass

	@staticmethod
	def getOnePeerFileList( peer ):
		ipAddr = peer
		if not isinstance( peer, str ):
			ipAddr = peer.getIp()
		else:
			ipAddr = peer
			pass
		s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		s.connect( (ipAddr,AllPeerInfo.port) )
		logging.info( 'getOnePeerFileList connected to '+ipAddr+' '+str(\
				AllPeerInfo.port) )
		dataSend = json.dumps( \
			dict( type='GFL', seq='0 0' ) )
		s.send( dataSend )
		s.settimeout( 500 )
		while True:
			try:
				dataGet = s.recv( RECVBUFFSIZE ) #todo warning too small?
				#dataGet = dataGet.strip()
			except socket.timeout:
				logging.info( 'time out when getOnePeerFileList( %s )', ipAddr )
				s.close()
				break
			else: #get the peer response
				try:
					dataGet = json.loads( dataGet )
				except ValueError:
					print 'getOnePeerFileList json.loads meet ValueError with\n'+str(dataGet)
					s.close()
					break
				if AllPeerInfo.parseDataGet:
					if ENDOFCONNECTION == AllPeerInfo().parseDataGet(\
							dataGet, (s,(ipAddr,AllPeerInfo.port)) ):
						s.close()
						break
			pass
