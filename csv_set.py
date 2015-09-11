#coding:utf-8

import sys
import csv
import codecs
import numpy as np

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdout = codecs.EncodedFile(sys.stdout, 'utf_8')
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

f = open(sys.argv[1], "rb")
data_reader = csv.reader(f)
#list_ = set()
list_1 = []
list_2 = []

for line in data_reader:
	line1 = line[0:4]
	line2 = line[1]
	#list_.add(line)
	list_1.append(line1)
	list_2.append(line2)

list_dict2 = dict(zip(list_2, range(0,len(list_2))))
#print list_1[list_dict2.values()]
for key in sorted(list_dict2.values()):
	print list_1[key]

#f = open('some.csv', 'w')
#writer = csv.writer(f, lineterminator='\n')
#
#writer.writerows(list)
#f.close()
