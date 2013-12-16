#coding=utf-8
import socket

#hostname = 'localhost'
hostname = '10.22.142.138'
port = 10087
serverSck = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
serverSck.bind( ( hostname, port ) )
serverSck.listen( 1 )

conSck, srcAddr = serverSck.accept()
print( 'connected to ', srcAddr )
import time 
dataGet = 'no data'
while 'quit' not in  dataGet and dataGet:  #如果输入了包含 quit 的内容,会断开连接. 可以使用telnet来测试 telnet localhost 10087
	dataGet = conSck.recv( 10 )
	print type( srcAddr )
	print( 'GET: {0} from {1} {2}'.format(dataGet, srcAddr, conSck) )
	t = time.localtime()
	conSck.send( 'I GET IT! '+dataGet+str(t.tm_hour)+str(t.tm_min) )

conSck.close()
serverSck.shutdown(socket.SHUT_RDWR)
serverSck.close()

