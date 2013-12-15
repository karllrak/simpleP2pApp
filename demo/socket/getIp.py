import socket, struct
def getIp():
	try:
		import fcntl
	except ImportError:
		return socket.gethostbyname( socket.gethostname() )
	else:
		s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
		return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', 'eth0' )
		)[20:24])

if __name__ == '__main__':
	print getIp()
