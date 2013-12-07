import os

if not os.path.isfile( 'dict.pdf'):
	print( 'No file dict.pdf' )
else:
	#info = os.stat( 'dict.pdf' )
	info = os.stat( 'nx.txt' )
	print( info )
