# -*- coding: utf-8 -*-5
"""
Created on Mon Sep 26 00:16:32 2016

Looked at following video to better understand stemming, the inverted index, 
and stop words:
https://www.youtube.com/watch?v=cY7pE7vX6MU

Referenced the following for regular expressions:
https://docs.python.org/2/library/re.html
https://regex101.com/

looked up os.lisdir(path) on:
http://stackoverflow.com/questions/18262293/python-open-every-file-in-a-folder

Looked at file-reading on: 
http://stackoverflow.com/questions/3906137/why-cant-i-call-read-twice-on-an-open-file

argv explanation from:
http://stackoverflow.com/questions/4117530/sys-argv1-meaning-in-script

Looked up measuring time from:
http://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
@author: jerry
"""

import os
import time
import json
import sys
import folderParser
import singleTermIndexer
import queryParser

#Getting current directory
currentDirectory = os.getcwd()

#TREC data path
dataPath = "TRECData/BigSample"
#Path where parsed documents are stored
corpusPath = "middleFiles/parsedDocs.txt"
#Location for unsorted/unmerged triples lists
unsortedTriplesPath = "middleFiles/unsortedTriples"
#Location for sorted triples
sortedTriplesPath = "middleFiles/sortedTriples"
#Location for Inverted Indexes
outputIndexPath = "indexes"
#Path of index to be stored
singleTermPath = "indexes/singleTermIndex.txt"


#Testing single term index
memory = 1000
start = time.time()
stIndexBuilder = singleTermIndexer.singleTermIndexer(dataPath, corpusPath, memory)
stIndexBuilder.buildIndex(unsortedTriplesPath, sortedTriplesPath, outputIndexPath)
end = time.time()
print("Elapsed Time: " + str(end - start) + " seconds")



print("Begin.py ended")