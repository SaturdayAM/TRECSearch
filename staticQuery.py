# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 02:30:41 2016

@author: jerry
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

testCosineVSM = cosineVSM.cosineVSM(parsedQueries, indexPath, cosineOutputPath, corpusPath)
testCosineVSM.getLexicon(lexiconPath)
testCosineVSM.retrieve()

end = time.time()

print("\n\nElapsed Time: " + str(end-start) + " seconds")
print("staticQuery.py ended")



#if(len(sys.argv) < 6):
#    print("Missing arguements")    
#else:
#    indexFolder = sys.argv[1]
#    queryPath = sys.argv[2]
#    retrievalModel = sys.argv[3]
#    indexType = sys.argv[4]
#    outputPath = sys.argv[5]
#
#print("staticQuery.py completed")