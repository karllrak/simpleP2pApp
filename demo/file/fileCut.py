#coding=utf-8
import os
import sys

filename = raw_input( 'Enter the file to cut (q to exit)')
while 'q' != filename and not os.path.isfile( filename ):
	print( '{0} is not a existing file. '.format( filename ) ),
	filename = raw_input( 'Enter the file to cut (q to exit)')

if 'q' == filename:
	sys.exit()
infos = os.stat( filename )
print( 'The file size of  {0} is {1}'.format( filename, infos.st_size ) )
piecesSum = int( raw_input( '你要把它大卸几块?' ) )
blocksize = infos.st_size / piecesSum
origFile = open( filename, 'r' )

for i in range( 1, piecesSum ): #the last part not dealed
	binData = origFile.read( blocksize )
	try:
		f = open( 'pycut'+str(i)+filename, 'w' )
		f.write( binData )
		f.close()
	except IOError:
		print( 'Oh no! IOError occured!' )

try:
	binData = origFile.read( infos.st_size - (piecesSum-1)*blocksize )
	fLast = open( 'pycut'+str(piecesSum)+filename, 'w' )
	fLast.write( binData )
	fLast.close()
except IOError:
	print( 'Oh no! IOError occured!' )

origFile.close()




