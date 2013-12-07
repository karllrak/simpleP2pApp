import sys
f = open( 'no.txt' )
if not f:
	print( 'No no.txt' )
	sys.exit()

i = 0
for lines in f:
	i = i + 1
	print( str(i)+lines )
close( f )
