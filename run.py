#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from os import walk
from os.path import join
import sqlite3

queryPath = "Y:\\SATATEST\\PN"
dbName = 'st_dt.db'
lastRt = ''
pnl = [] # pn list
fl = [] # file list
dtl = [] # duration time list
wototcnt = 0

conn = sqlite3.connect(dbName)
print ('Opened database successfully')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS " + dbName)
conn.commit()
c.execute("CREATE TABLE IF NOT EXISTS log(PN CHAR(60) NOT NULL, MAX INT, MIN INT, AVG REAL, PRIMARY KEY(PN))")
conn.commit()


def hms2sec(st):
	h, m, s = st.split(':')
	return (int(h) * 3600) + (int(m) * 60) + int(s)

pnl = os.listdir(queryPath)
print("PN LIST = ", pnl)

for pn in pnl:
	dtl.clear()
	if '.' in pn:
		continue
	elif 'SN' in pn:
		continue
	goal = queryPath + '\\' + pn
	print("query pn = ", goal)
	for root, dirs, files in walk(goal):
		# print(dirs)
		for f in files:
			if '.log' not in f:
				continue
			if lastRt != root:
				lastRt = root
				fullpath = join(root, f)
				# print(fullpath)
				r, satatet, pnf, pn, wo, fileLog = fullpath.split('\\')
				# print(r, satatet, pnf, pn, wo, fileLog)
				if '2' in wo[0]:
					# print("2 ", wo)
					continue
				wototcnt = wototcnt + 1
				file = open(fullpath, 'r')
				fl = file.readlines()    
				file.close()
				#print(fl)
				for x in fl:
					#print(x)
					if 'Duration ' in x:
						# print(x)
						#print(x.split(' ')[1])
						# print(x.find(' '))
						st = x[x.find(' ') + 1:None]
						#print(st)
						sec = hms2sec(st)
						# print(sec)
						dtl.append(sec)
			else:
				continue
	try:
		M = max(dtl)
		m = min(dtl)
		a = round((sum(dtl)/len(dtl)), 2)
		# print("max = ", M)				
		# print("min = ", m)					
		# print("avg = ", a)
	except:
		print("dlt is empty!")
		continue

	try:
		c.execute("INSERT INTO log('PN', 'MAX', 'MIN', 'AVG') VALUES(?, ?, ?, ?)", (pn, M, m, a))
		conn.commit()
	except:
		print("Insert DB error!")
	print(wototcnt)
conn.close()




		  

