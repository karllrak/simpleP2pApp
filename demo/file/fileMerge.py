import os

filename = raw_input( 'Enter the filename(such as nx.txt)')

i = 1
mergedFile = open( 'pyMerged'+filename, 'w' )

while True:
	partFileName = 'pycut'+str(i)+filename
	if not os.path.isfile( partFileName ):
		print( 'Oops! {0} is missing!'.format( partFileName ) )
		break;
	fpart = open( partFileName, 'r' )
	binData = fpart.read()
	mergedFile.write( binData )
	fpart.close()
	i = i + 1

mergedFile.close()
