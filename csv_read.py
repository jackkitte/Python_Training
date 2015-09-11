#coding:utf-8

import sys
import csv
import codecs
import numpy as np

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
def nparray_generate(file):
	sys.stdout = codecs.EncodedFile(sys.stdout, 'utf_8')
	sys.stdin = codecs.getreader('utf_8')(sys.stdin)
	
	f = open(file, "rb")
	data_reader = csv.reader(f)
	list = []
	
	for line in data_reader:
		#line = line[0:3] + line[7:9]
		line = line[1]
		list.append(line)
	
	nparray = np.array(list)
	return nparray
	
	#f = open('some.csv', 'w')
	#writer = csv.writer(f, lineterminator='\n')
	#
	#writer.writerows(list)
	#f.close()
