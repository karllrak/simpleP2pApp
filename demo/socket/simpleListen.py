#coding=utf-8
import socket

hostname = 'localhost'
port = 10087
serverSck = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
serverSck.bind( ( hostname, port ) )
serverSck.listen( 1 )

conSck, srcAddr = serverSck.accept()
print( 'connected to ', srcAddr )

dataGet = 'no data'
while 'quit' not in  dataGet and dataGet:  #如果输入了包含 quit 的内容,会断开连接. 可以使用telnet来测试 telnet localhost 10087
	dataGet = conSck.recv( 10 )
	print( 'GET: {0} from {1}'.format(dataGet, srcAddr) )
	conSck.send( 'I GET IT!' )

conSck.close()

