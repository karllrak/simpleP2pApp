import hashlib

f = open( '../file/nx.txt' )
data = f.read() 
print hashlib.sha1(data).hexdigest()
f.close()
