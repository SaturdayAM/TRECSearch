# -*- coding: utf-8 -*-
"""
Translates documents and queries into vector space. Calculates and ranks
searches by cosine similarity scores. Returns an array of N top documents.
Does the same thing as the normal cosineVSM.py file.

"""
import numpy as np
import re
import json
import math
import operator

class initialCosineVSM():
    
    def __init__(self, parsedQueries, nTopDocs, indexPath, corpusPath,
                 lexiconPath):
        self.parsedQueries = parsedQueries
        self.nTopDocs = int(nTopDocs)
        self.index = np.load(indexPath).item()
        self.corpusPath = corpusPath
        self.lexicon = np.load(lexiconPath).item()
        self.rankArray = []

    #--------------------------------------------------------------------------     
    #                        Main Retrieval Function 
    #--------------------------------------------------------------------------
    def retrieve(self):
        print("initialCosineVSM.retrieve()")

        for query in self.parsedQueries:
            #Store document scores on dict, rankings on list
            docScores = dict()
            docRankings = []
            
            #Regular expressions to extract IDs from parsed docs
            #Store doc IDs in a dictionary to associate with their scores
            docIDExtract = re.compile("FR[0-9]{6}-[0-9]-[0-9]{5}")
            parsedDocs = open(self.corpusPath)
            numDocs = 0
            for document in parsedDocs:
                docId = docIDExtract.findall(document)
                docIdStr = ''.join(docId)
                docScores[docIdStr] = {'numerator': 0, 'denomOne': 0,
                                       'denomTwo': 0, 'finalScore': 0}
                numDocs += 1            
            
            
            #Temp store each query in a dictionary for convenient way
            #to count term frequencies
            queryNo = 0
            tempQueryDict = dict()
            for i, token in enumerate(query.split()):
                #Get query no
                if i == 0:
                    queryNo = str(query.split()[0])
                #Count up query term frequencies
                else:
                    term = query.split()[i]
                    if term not in tempQueryDict:
                        tempQueryDict[term] = 1
                    else:
                        tempQueryDict[term] += 1

            #-----------------------Calculating Scores-------------------------
            #Calculating denominator score portion for query
            queryDenomScore = 0;
            for term in tempQueryDict:
                #Components of our tf-idf scores
                queryTf = tempQueryDict[term]
                termDf = 0
                termIdf = 0                

                
                #If term is not in lexicon, then the Df will be 0 and score
                #will not be affected
                if term not in self.lexicon:
                    termDf = 0
                else:
                    #It is in lexicon, need to get the termID and find term Df
                    termId = str(self.lexicon[term])
                    
                    #use termID to get postings list.
                    #For each document key in the postings list
                    for document in self.index[termId]:
                        #iterate termDf
                        termDf += 1
                    #Repeat, now calculating the scores for each document
                    #In the postings list
                    
                    #Calculate idf for the term
                    if termDf == 0:
                        termIdf = 0
                    else:
                        termIdf = math.log10(numDocs/termDf)
            
                queryDenomScore += (queryTf*termIdf)
            
            queryDenomScore = queryDenomScore**2
            
            #After getting query term frequencies,
            #for each term in the dictionary, get the postings list in index
            for term in tempQueryDict:
                #Components of our tf-idf scores
                queryTf = tempQueryDict[term]
                termDf = 0
                termIdf = 0                

                if term not in self.lexicon:
                    termDf = 0
                else:
                    #It is in lexicon - need to get the termID and find term Df
                    termId = str(self.lexicon[term])

                    #use termID to get postings list.
                    #For each document key in the postings list
                    for document in self.index[termId]:
                        #iterate termDf
                        termDf += 1
                    #Repeat, now calculating the scores for each document
                    #In the postings list
                    
                    #Calculate idf for the term
                    if termDf == 0:
                        termIdf = 0
                    else:
                        termIdf = math.log10(numDocs/termDf)
                    
                    for document in self.index[termId]:
                                             
                        docTf = self.index[termId][document]
                              
                        numerator = (queryTf*termIdf)*(docTf*termIdf)
                        denomPartOne = (docTf*termIdf)**2
                        
                        #update the relevant components of cosineVSM   
                        docScores[document]['numerator'] += numerator
                        docScores[document]['denomOne'] += denomPartOne
                        docScores[document]['denomTwo'] = queryDenomScore

            for document in docScores:
                numerator = docScores[document]['numerator']
                denomOne = docScores[document]['denomOne']
                denomTwo = docScores[document]['denomTwo']
                denominator = math.sqrt(denomOne+denomTwo)
                
                
                if denominator == 0:
                    finalScore = 0
                else:
                    finalScore = numerator/denominator
                docScores[document]['finalScore'] = finalScore
                
            
            #Now, for each given query, we need to get the top 100 results
            #First, add the documents with their scores into our array
            for document in docScores:
                #Create string with the query number, doc number, and score
                rankingString = (str(queryNo) + " " + document + " " 
                                + str(docScores[document]['finalScore']))
                #Append to array
                docRankings.append(rankingString)
                
            #Sort the array
                docRankings.sort(key=lambda line: float(line.split()[2]),
                                 reverse = True)
            
            topNDocs = docRankings[:self.nTopDocs]            
            
            self.rankArray.append(topNDocs)
        
        return self.rankArray


        