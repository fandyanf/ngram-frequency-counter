# ngram-frequency-analysis

This is a badly-written, overcomplicated python script that parses files and exports the frequency of n-grams. In other words, n-word phrases.

### Some Information

  -lets you analyze more than one text file. whoop-de-do.
  -script probably won't break if you have it parse 10gb of files
  -Python version 3
	-uses sqlite, because my sins are already taking me to hell so i might as well accelerate the process

### How To Use
    -get python 3
    -put desired text files into the folder titled, "input"
    -run frequency.py
    -wait an unnecessary amount of time for it to chew through the files 
    -get analysis in csv files in the export folder
		
#### Defaults
		-1-word and 2-word phrases are analyzed.
		-to change it, change plengths=
		-want only one n-word phrase to be analyzed? it should look like this: (x,)
		  -where x is the number of words
			-comma is there so that variable remains a list instead of an integer
	-common 1-word phrases are excluded
		-to change it so that they are included, change exclude1 = True
		-to change which words are excluded, edit excludelength1.txt in the phrasestoexclude folder
		-"stop words" were taken from http://ir.dcs.gla.ac.uk/resources/linguistic_utils/
### Code Licensing
The script is under the Passive-Aggressive (v2) license. See license.txt .

### Sample Text Licensing
The poem, Childe Roland To The Dark Tower Came is in the public domain.

The other two texts, the Federalist Papers and The Adventures of Sherlock Holmes, are distributed under the Project Gutenberg License.

#### To-Do List
	
	-script can exclude phrases of any length
	-figure out if using .csvs work faster than sqlite, and if they're worth the effort 
#### Timeline
	2016-07-14 Made a script, shoddy but functional (in the sense that wind erosion functions as sandpaper)
	2016-07-15 Nuked my old repo (phrase-frequency-analysis) and half the script because it was embarassingly terrible.
	2016-07-16 Moved what remained of the old script (lost some stuff due to ragequitting) into testfolder
	2016-07-18 Made a more efficient but incomplete n-gram counter.
  2016-07-21 Finished the basic script, but doesn't auto-sort,exclude, or limit ranks