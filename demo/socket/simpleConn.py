#coding=utf-8

import socket as sk
s = sk.socket( sk.AF_INET, sk.SOCK_STREAM )
hostname = 'localhost'
port = 10087
#s.bind( (hostname,port) )
s.connect( (hostname,port) )
dataGet = 'da'
while dataGet and 'quit' not in dataGet:
	s.send( raw_input( 'Send to '+hostname ) )
	dataGet = s.recv( 100 )
	print dataGet

s.close()


