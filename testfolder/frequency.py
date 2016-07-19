#just a reminder, this is python 3

import glob
import time
import re
import fileinput
import random

import sys
import fuckit
import os

#
import sqlite3
open(".\\temp.db","w+")
conn = sqlite3.connect('temp.db')
c = conn.cursor()
#

foldername = "input"
dirpath = ".\\"+ foldername + "\\*"
inputlist = glob.glob(dirpath)

###
plengths = (1,2)
minfreq = 5 #False or number
minrank = False #False or number,
exclude1 = True
###

###DEBUG
deletetemps = True
###DEBUG

def filetest(string):
	filehandle=open(".\\testfolder\\ayy.txt","w+")
	filehandle.write(string)
	filehandle.close()	
	print("writetest is being used")

def appendtest(words):
	filehandle=open(".\\testfolder\\ayy.txt","w+")
	for item in words:
		filehandle.write("%s\n" % item)
	filehandle.close()	
	print("append def is being accessed")
	
def create_tablenames(plengths):
	#also creates final exported files
	tablenames=dict()
	for x in plengths:
		if type(1) != type(x): sys.exit("plengths has values that aren't digits")
		if (x > 15) and (pls_delimiter == True): sys.exit("plengths has values that are too big.")
		#else: pass
		tablenames[x] = "templength" + str(x) + ".txt"
		temp = open(tablenames[x],"w+")
		temp.close()
		temp = open(".\\export\\length"+str(x)+".txt","w+")
		temp.close
	return tablenames


def sanitize(string):
	placeholder = "wubbalubbadubdub1251"
	string = re.sub(r"-", r" ", string)
	string = re.sub("('|’)", placeholder, string)
	string = re.sub(r'([^0-9a-zA-Z])+', ' ', string)
	string = re.sub(placeholder, "'",string)
	string = string.lower()
	string = re.sub(r"\r|\n",r" ", string)
	for i in range(15): string = re.sub("(  |   |     )"," ", string)
#	filetest(string)
	words = string.split()
	return words

def compile_exclude1():
	excludeonelist = list()
	with open(".\\phrasestoexclude\\excludelength1.txt","r") as exfile:
		for line in exfile:
			phrase = line.strip("\r")
			phrase = phrase.strip("\n")
			excludeonelist.append(phrase)
	return excludeonelist

#if exclude1 == True: excludeonelist = compile_exclude1()
#else: excludeonelist = ("",)	
#print(excludeonelist)
			
def create_lists(inputlist,tablenames):
	if exclude1 == True: excludeonelist = compile_exclude1()
	
	numoflines = 0
	for filepath in inputlist:
		print("processing this file:", filepath, end='')
		filehandle = open(filepath,"r+")
		filestring = filehandle.read()
		
		words = sanitize(filestring)
		
#		for x in plengths: open(".\\length"+str(x)+".txt","w+")
		for x in plengths:
			tablehandle = open(tablenames[x],"a")
			for i in range(len(words)-(x-1)):
				phrase = " ".join(words[i:(i+x)])
				if x == 1 and exclude1 == True:
					if phrase in excludeonelist: continue
				#phrase = phrase.strip("\r")
				tablehandle.write("%s\n" % phrase)
				numoflines = numoflines+1
			tablehandle.close
		print(" done.")
		filehandle.close
	return numoflines

tablenames = create_tablenames(plengths)

numoflines = create_lists(inputlist,tablenames)

print("Now finding frequencies of phrases...")
print(str(numoflines) + " lines to process")

currentline = 0

#time.sleep(5)
times = 0
for x in plengths:
##	
	c.execute("DROP TABLE IF EXISTS counts")
	c.execute("CREATE TABLE counts (phrase TEXT, count INTEGER)")
<<<<<<< HEAD
##	
	phrasefile = tablenames[x]
	
	infile = open(phrasefile,"r")
	searchfile = open(phrasefile,"r")
	num = 0
	print("finding frequencies for "+str(x)+"-word phrases...")
	for line in infile:
		currentline += 1
#		phrase = line.strip("\n")
#		phrase = line.strip("\r")
		
		if (currentline/numoflines)*100 > num:
			percentage = str(round((currentline/numoflines)*100,3))
			print(percentage, "%", end = "\r")
			num+=6
	print(str(round((currentline/numoflines)*100,3)), "%")
	
	
	
	try:
		infile.close()
		searchfile.close()
		if deletetemps == True: os.remove(phrasefile)
	except:
		print(phrasefile, "isn't getting deleted; still in use somewhere.")
	'''	
=======
	with open(phrasefile,"r+") as infile:
		for line in infile:
			start = time.time()
			
			currentline = currentline + 1
			#print("accessing line",currentline, "out of", numoflines)
			phrase = line.strip("\n")
			phrase = line.strip("\r")
			#print(phrase)
			#continue
			c.execute('SELECT count FROM counts WHERE phrase = ? ', (phrase, ))
			row = c.fetchone()
#			row = None
			#print(row)
			if row is None:
				c.execute('INSERT INTO counts (phrase, count) VALUES ( ?, 1 )', ( phrase, ) )
			else:
				c.execute('UPDATE counts SET count=count+1 WHERE phrase = ?', (phrase, ))
			print(str(round((currentline/numoflines)*100,3)), "%", end="\r")
			# +str(currentline) , end="\r")
			end = time.time()
			times = times + (end-start)
	print(str(round((currentline/numoflines)*100,3)), "%")
	if deletetemps == True: os.remove(phrasefile)
	
>>>>>>> parent of d41bd46... retain sql, extra sanitation
	print("Sorting data for", str(x) + "-length phrases...", end="")
	if minfreq != False: c.execute("DELETE FROM counts WHERE count < ?",(minfreq,))
	c.execute('CREATE TABLE ordered_counts as SELECT * FROM counts ORDER BY count DESC')
	if deletetemps == True: c.execute("DROP TABLE IF EXISTS counts")

	if minrank == False: c.execute('SELECT * FROM ordered_counts')
	else: c.execute('SELECT * FROM ordered_counts LIMIT 0,?',(minrank,))
	print(" Done.")
	
	print("Exporting data for", str(x) + "-length phrases...", end="")
	analysis = open(".\\export\\length"+str(x)+".txt","a")
	relevantdata = c.fetchall()
	rank = 0
	for row in relevantdata:
		rank = rank+1
		phrase = str(row[0].strip("\n"))
		count = str(row[1])
		pac = str(rank)+ "\t" + count+"\t"+phrase
		analysis.write("%s\n" % pac)
	#for row in c.execute('SELECT * FROM ordered_counts LIMIT 0,?',(minrank,))
<<<<<<< HEAD
	'''
#
	c.execute("DROP TABLE IF EXISTS ordered_counts")
#
=======
			
	if deletetemps == True: c.execute("DROP TABLE IF EXISTS ordered_counts")
>>>>>>> parent of d41bd46... retain sql, extra sanitation
	print(" Done.")
	
conn.commit()
conn.close()
time.sleep(.10)
#print(times,numoflines)
if deletetemps == True:
	print("removing temp files...")
#	for length in plengths: os.remove(tablenames[length])
	try: os.remove("temp.db")
	except: print("temp.db is in use. won't get deleted.")
	
#So it's finally come, you have left my world
#But i'll miss mine, my darling girl
#I held your head, kissed your lovely brow
#And bid farewell, you're sailing now