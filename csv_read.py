#coding:utf-8

import sys
import csv
import codecs

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdout = codecs.EncodedFile(sys.stdout, 'utf_8')
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

f = open(sys.argv[1], "rb")
data_reader = csv.reader(f)
list = []

for line in data_reader:
	line = line[0:3] + line[7:9]
	list.append(line)

f = open('some.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

writer.writerows(list)
f.close()
