# -*- coding: utf-8 -*-5
"""
Creates a single term index. 
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
memory = 1000 # param for no. of lists per file prior to merging
start = time.time()
stIndexBuilder = singleTermIndexer.singleTermIndexer(dataPath, corpusPath, 
													 memory)
stIndexBuilder.buildIndex(unsortedTriplesPath, sortedTriplesPath,
													 outputIndexPath)
end = time.time()
print("Elapsed Time: " + str(end - start) + " seconds")


print("Begin.py ended")