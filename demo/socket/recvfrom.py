import socket as sk
sServer = sk.socket( sk.AF_INET, sk.SOCK_DGRAM )
hostname = 'localhost'
port = 10087
sServer.bind( (hostname,port) ) # no need to listen ...

import time
def recvTimeout( sServer ):
	time.sleep( 0.5 )
	sServer.close()
	print 'sServer closed'
	pass
from threading import Thread
#closeThrd = Thread( target=recvTimeout, args=(sServer,) )
#closeThrd.start()
sServer.settimeout( 1 )
try:
	data, address = sServer.recvfrom( 100 )
except sk.timeout:
	print 'Timeout!'
else:
	print 'GET ', data, ' from ', address
finally:
	sServer.close()



