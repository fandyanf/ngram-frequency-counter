#!/usr/bin/env python3

import glob
import time
import re
import fileinput
import random
import sys
#import shutil
import sqlite3
import os

###DEBUG
deletetemps = False
maxchunksize = 20000 #determines how many phrases can be in a list before they're written to the table
retrievechunksize = 4000 #determines how many phrases can be retrieved from the table at a time

if os.name == 'nt':
    Windows = True
else:
    Windows = False
###DEBUG

foldername = "input"
dirpath = ".\\"+ foldername + "\\*"
if Windows == False: dirpath = "./"+foldername+"/*"
inputlist = glob.glob(dirpath)

###
plengths = (1,2)
minfreq = 5 #False or number
minrank = False #False or number,
exclude1 = True
###


	
def check_plengths(plengths):
#	ngramlists=dict()
#	analyses=dict()
	for x in plengths:
		if type(1) != type(x): sys.exit("plengths has values that aren't digits")
		if (x > 15) and (pls_delimiter == True): sys.exit("plengths has values that are too big.")

def setup_databases(plengths):
	databases = dict()
	connections = dict()
	cursors = dict()
	for n in plengths: 
		databases[n] = str(n) + ".sqlite3"
		open(databases[n],"w+",encoding = "ISO-8859-1")
		
		connections[n] = sqlite3.connect(databases[n])
		cursors[n] = connections[n].cursor()
		
		c = cursors[n]
		c.execute("DROP TABLE IF EXISTS phrases")
		c.execute("CREATE TABLE phrases (gram TEXT)")
	return databases, connections, cursors

def sanitize(string):
	placeholder = "wubba1251"
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
	#used in create_lists
	excludeonelist = list()
	if Windows == True: fp = ".\\phrasestoexclude\\excludelength1.txt"
	elif Windows == False: fp = "./phrasestoexclude/excludelength1.txt"
	with open(fp,"r",encoding = "ISO-8859-1") as exfile:
		for line in exfile:
			phrase = line.strip("\r")
			phrase = phrase.strip("\n")
			excludeonelist.append(phrase)
	return excludeonelist

def addtodatabase(phrases,c,n):
	#n being the number of words in the phrase
	#print(phrases)
	
	pass

def create_sortedlists(inputlist,cs,conns):
	if exclude1 == True: excludeonelist = compile_exclude1()
	
	numoflines = dict()
	for n in plengths: numoflines[n] = 0
	
	for filepath in inputlist:
		print("processing this file:", filepath, end='')
		time.sleep(.001)
		filehandle = open(filepath,"r",encoding = "ISO-8859-1")
		filestring = filehandle.read()
		
		words = sanitize(filestring)
		
		for x in plengths:
			current_chunk_size = 0
			phrase_chunk = list()
			for i in range(len(words)-(x-1)):
				phrase = " ".join(words[i:(i+x)])
				if (x == 1 and exclude1 == True and phrase in excludeonelist): continue

				phrase = phrase.strip("\r")
				phrase = phrase.strip("\n")
				#tablehandle.write("%s\n" % phrase)
				
				phrase_chunk.append((phrase,))
				numoflines[x] = numoflines[x]+1
				current_chunk_size += 1
				if current_chunk_size == maxchunksize: 
					cs[x].executemany("INSERT INTO phrases (gram) VALUES (?)", phrase_chunk)
					phrase_chunk = list()
					current_chunk_size = 0
				elif current_chunk_size <= maxchunksize: pass #don't put "current_chunk_size += 1" here, otherwise phrase_chunk is actually max+1 phrases
				else: sys.exit("something wrong with the current chunk counter")
			cs[x].executemany("INSERT INTO phrases (gram) VALUES (?)", phrase_chunk)
		print(" done.")
		filehandle.close
	print("done processing files.")

	print("writing phrases to disk and alphabetizing...",end="")
	for x in plengths: 
		cs[x].execute('CREATE TABLE sorted_phrases as SELECT * FROM phrases ORDER BY gram ASC')
		if deletetemps == True: cs[x].execute('DROP TABLE phrases')
		conns[x].commit()
	print(" done.")
	time.sleep(.001)
	return numoflines

check_plengths(plengths)
databases, conns, cs = setup_databases(plengths)
numoflines = create_sortedlists(inputlist,cs,conns)

print("finding frequencies of phrases...",end="")
time.sleep(.001)

analyses = dict()
for n in plengths:
	phrases = list()
	
	analysis_name = ""+str(n)+".csv"
	if Windows == False: analyses[n] = "./output/length"+analysis_name+""
	elif Windows == True: analyses[n] = ".\\output\\"+analysis_name+""
	
	open(analyses[n],"w+",encoding="utf8")
	analysis_handle = open(analyses[n],"a+",encoding="utf8")
	
	#frequencies = open(r"./output/length"+str(n)+".csv","a+",encoding="utf8")
	while True:
		if len(phrases) < 5:
			cs[n].execute("SELECT * FROM sorted_phrases LIMIT(?)", (retrievechunksize,))
			phrases.extend(cs[n].fetchall())
			cs[n].execute("DELETE FROM sorted_phrases WHERE ROWID IN (SELECT ROWID FROM sorted_phrases LIMIT (?))", (retrievechunksize,))
			#print("adding")
		if len(phrases) <= 2:break
		
		phrase = phrases[1]
		phrases.remove(phrases[1])
		
		if phrase == phrases[len(phrases)-1]:
				try: rollover += len(phrases)
				except: rollover = len(phrases)
				phrases = [phrase,]
				continue
			
		count = 1
		while True:
			#print(len(phrases))
			if phrase != phrases[1]:
				try: count += rollover
				except: pass
				###print(phrase, count)
				analysis_handle.write(str(count)+"\t"+str(phrase)+"\n")
				count = 0
				rollover = 0
				break
			elif phrase == phrases[1]:
				count += 1
				phrases.remove(phrases[1])
			else: sys.exit("something went wrong",phrase,count,rollover)
print(" done.")


for x in plengths:
	if deletetemps == True:
		print("removing " + databases[x]+"...")
		try: os.remove(databases[x])
		except: print(str(databases[x])+" is in use. won't get deleted.")
	conns[x].close()

#I almost forgot to say something else
#But if I can't fit it in, i'll keep it all to myself
#I almost referenced you, in my code today
#But then I deleted the egg and replaced it with Cake