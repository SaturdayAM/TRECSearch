# -*- coding: utf-8 -*-
"""
Implementation of pseudo-relevance feedback. 

@author: jerry
"""
import cosineVSM
import initialCosineVSM
import re
import heapq

class pseudoRelater():
    
    def __init__(self, queries, nTopDocs, tTopTerms, indexPath, expandedOutput, corpusPath, lexiconPath):
        self.queries = queries
        self.nTopDocs = nTopDocs
        self.tTopTerms = tTopTerms
        self.indexPath = indexPath
        self.outputPath = expandedOutput
        self.corpusPath = corpusPath
        self.lexiconPath = lexiconPath
        self.finalExpansions = []
        
        
        
    def pseudoRelate(self):
        stopWordList = ["the", "and", "of", "to", "a", "for", "in", "be", "that", "is", "as", "on", "or", "not", "this"]                                
                                
        #Initial cosineVSM retrieval, gets the top N Documents
        print("Commencing initial cosineVSM")
        initialRetrieval = initialCosineVSM.initialCosineVSM(self.queries, self.nTopDocs, self.indexPath, self.corpusPath, self.lexiconPath)
        topNDocArray = initialRetrieval.retrieve()
        
            
        #An array to correspond for each term to append things
        
        #Get just the top N Doc IDs for each of the queries
        nDocIds = []
        for i, doc in enumerate(topNDocArray):
            nDocuments = []
            docList = topNDocArray[i]
            for docString in docList:
                stringTokens = docString.split()
                nDocuments.append(stringTokens[1])
            nDocIds.append(nDocuments)
        
        #Now you need to get the top terms of the top N Documents and update the queries
        parsedDocs = open(self.corpusPath)        
                
        expandedQueries = []       
        bracketRemove = re.compile("\[")
        
        for relevantDocs in nDocIds:
            #to store a single queries' expanded terms
            singleExpansion = ""
                        
            
            #For each top document, get the top t terms
            #Looked up sorting dictionaries at:
            #   http://stackoverflow.com/questions/7197315/5-maximum-values-in-a-python-dictionary
            for docId in relevantDocs:
                regexString = "\( " + docId + "(.*?)\]\)"
                matchedDocuments = ""
                for line in parsedDocs:   
                    matches = re.findall(regexString, line)
                    if len(matches) > 0:
                        matchedDocuments = "".join(matches)
                parsedDocs.seek(0)
                docStr = bracketRemove.sub(' ', matchedDocuments)               
                
                tempDocDict = dict()
                for token in docStr.split():
                    if token not in stopWordList:
                        if token not in tempDocDict:
                            tempDocDict[token] = 1
                        else:
                            tempDocDict[token] += 1
                topTerms = heapq.nlargest(int(self.tTopTerms), tempDocDict, key=tempDocDict.get)
                singleExpansion = singleExpansion + ' ' + ' '.join(topTerms)
            
            expandedQueries.append(singleExpansion)
                
        
        for i, query in enumerate(expandedQueries):
            expandedStr = self.queries[i] + " " + expandedQueries[i]
            self.finalExpansions.append(expandedStr)
            
#        #Final step is to run VSM on the expanded queries
        secondCosineVSM = cosineVSM.cosineVSM(self.finalExpansions, self.indexPath, self.outputPath, self.corpusPath)
        secondCosineVSM.getLexicon(self.lexiconPath)
        secondCosineVSM.retrieve()
            



