import sys
import os

#please search  TOCTTOU 
# time of check to time of use
f = None
try:
	f = open( 'no.txt' )
except IOError:
	if not f:
		print( 'No no.txt' )
		newFileName = raw_input( 'Enter another filename q to quit' )
		while 'q' != newFileName and not os.path.isfile( newFileName ):
			newFileName = raw_input( 'Enter another filename q to quit' )

		if 'q' == newFileName:
			sys.exit()
		else:
			try:
				f = open( newFileName )
			except IOError:
				print( 'Oops! The file {0} meet a TOCTTOU'.format(newFileName) )
finally:
	i = 0
	if not f:
		sys.exit()

	for lines in f:
		i = i + 1
		print( str(i)+lines ), # note that(haha) there is a comma which means no newline
	f.close()
