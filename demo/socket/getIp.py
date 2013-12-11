import socket, struct
try:
	import fcntl
except ImportError:
	print socket.gethostbyname( socket.gethostname() )
else:
	s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
	print socket.inet_ntoa(fcntl.ioctl(
	s.fileno(),
	0x8915,  # SIOCGIFADDR
	struct.pack('256s', 'eth0' )
	)[20:24])
