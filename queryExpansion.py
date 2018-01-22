# -*- coding: utf-8 -*-
"""
Python file to run the search engine with query expansion.
Step occurs after the index and lexicon have been created.


@author: jerry
"""
import pseudoRelater
import queryParser
import cosineVSM
import time
import sys


indexPath = "indexes/singleTermIndex.npy"
queryPath = "TRECData/QueryFile/queryfile.txt"
expandedOutputPath = "rankings/expandedCosineVSM.txt"
corpusPath = "middleFiles/parsedDocs.txt"
lexiconPath = "middleFiles/lexicon.npy"

print("\nImplementing query-expanded search: ")
if(len(sys.argv) < 3):
    print("Must enter parameters for N (numDocs), T (numTerms)")
    sys.exit()
    
nTopDocs = sys.argv[1]
tTopTerms = sys.argv[2]    
    
print("N Top Docs: ", nTopDocs)
print("T Top Terms: ", tTopTerms)
print("Outputing results to: " + expandedOutputPath)

start = time.time()

#1. Parse the queries for the first time
initialQParse = queryParser.queryParser(queryPath)
initialQParse.parseQuery()
initialQueries = initialQParse.parsedQueries


#2. Pass the parsed queries to our query expansion algorithm
queryExpander = pseudoRelater.pseudoRelater(initialQueries, nTopDocs, tTopTerms
				, indexPath, expandedOutputPath, corpusPath, lexiconPath)
queryExpander.pseudoRelate()

end = time.time()
print("\n\nElapsed Time: " + str(end-start) + " seconds")
print("queryExpansion.py ended")

#1. Pass query path to pseudoRelater, pseudoRelater:
    #2. Parses the queries
    #3. Run cosineVSM on the queries
    #4. Gets the nTopDocs and tTopTerms
    #5. Runs cosineVSM on these new queries

