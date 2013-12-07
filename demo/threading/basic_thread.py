#coding=utf-8
import time
import random
from threading import Thread

g_rand = random.Random() 
#随机数

def thread_fxn( tid ):
	for i in range( 0, 10 ):
		print( 'thread %0 sleeps...zzz'% tid )
		time.sleep( g_rand.randint(2,6)/6 )

for i in range( 0, 6 ):
	t = Thread( target=thread_fxn, args=(i,) )
	t.start()
