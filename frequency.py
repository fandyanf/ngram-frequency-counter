import glob
import time
import re
import fileinput
import random
import sys
import shutil
#import fuckit
import sqlite3
import os

foldername = "testfolder"
dirpath = ".\\"+ foldername + "\\*"
inputlist = glob.glob(dirpath)

###
plengths = (1,)
minfreq = 5 #False or number
minrank = False #False or number,
exclude1 = True
###

###DEBUG
deletetemps = False
maxchunksize = 20000 #determines how many phrases can be in a list before they're written to the table
retrievechunksize = (10,) #determines how many phrases can be retrieved from the table at a time
###DEBUG
	
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
		open(databases[n],"w+")
		
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
	with open(".\\phrasestoexclude\\excludelength1.txt","r") as exfile:
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
		filehandle = open(filepath,"r")
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

	print("writing phrases to disk and alphabetizing...")
	for x in plengths: 
		cs[x].execute('CREATE TABLE sorted_phrases as SELECT * FROM phrases ORDER BY gram ASC')
		if deletetemps == True: cs[x].execute('DROP TABLE phrases')
		conns[x].commit()
	print("done	with that.")
	return numoflines

check_plengths(plengths)
databases, conns, cs = setup_databases(plengths)
numoflines = create_sortedlists(inputlist,cs,conns)

n=1

templimit = 100

phrases = list()
while True:
	if len(phrases) < templimit:
		cs[n].execute("SELECT * FROM sorted_phrases LIMIT(?)", (templimit,))
		phrases.extend(cs[n].fetchall())
		cs[n].execute("DELETE FROM sorted_phrases WHERE ROWID IN (SELECT ROWID FROM sorted_phrases LIMIT (?))", (templimit,))
	if len(phrases) == 0:break

	phrase = phrases[1]
	phrases.remove(phrases[1])
	count=1
	rollover = 0

	while True:
		if phrase != phrases[1]:
			print(count,phrase)
			break
		elif phrase == phrases[1]:
			count = count+1
			phrases.remove(phrases[1])
'''

			try: 
				tmp = phrases[1]
			except:
				cs[n].execute("SELECT * FROM sorted_phrases LIMIT(?)", (templimit,))
				phrases.extend(cs[n].fetchall())
				cs[n].execute("DELETE FROM sorted_phrases WHERE ROWID IN (SELECT ROWID FROM sorted_phrases LIMIT (?))", (templimit,))
'''
for x in plengths:
	if deletetemps == True:
		print("removing " + databases[x]+"...")
		try: os.remove(databases[x])
		except: print(str(databases[x])+" is in use. won't get deleted.")
	conns[x].close()
	
print