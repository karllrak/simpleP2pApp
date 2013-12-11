#coding=utf-8
import time
import random
from threading import Thread

g_rand = random.Random() 
#随机数

def thread_fxn( tid ):
	localVar = tid
	for i in range( 0, 10 ):
		print( 'thread %0d sleeps..%d .times'% (tid,i) )
		print 'localVar is %d' % localVar
		time.sleep( g_rand.randint(2,6)/6 )

for i in range( 0, 6 ):
	t = Thread( target=thread_fxn, args=(i,) )
	t.start()
