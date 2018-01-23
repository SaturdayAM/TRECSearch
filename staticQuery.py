# -*- coding: utf-8 -*-
"""
Python file to run the search engine without query expansion. 
Step occurs after index and lexicon are created.

"""

import sys
import numpy as np
import queryParser
import cosineVSM
import time

indexPath = "indexes/singleTermIndex.npy"
queryPath = "TRECData/QueryFile/queryfile.txt"
cosineOutputPath = "rankings/cosineVSM.txt"
corpusPath = "middleFiles/parsedDocs.txt"
lexiconPath = "middleFiles/lexicon.npy"


start = time.time()

testQueryParser = queryParser.queryParser(queryPath)
testQueryParser.parseQuery()
parsedQueries = testQueryParser.parsedQueries

testCosineVSM = cosineVSM.cosineVSM(parsedQueries, indexPath, cosineOutputPath,
									corpusPath)
testCosineVSM.getLexicon(lexiconPath)
testCosineVSM.retrieve()

end = time.time()

print("\n\nElapsed Time: " + str(end-start) + " seconds")
print("staticQuery.py ended")

