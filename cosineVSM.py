# -*- coding: utf-8 -*-
"""
Translates documents and queries into vector space. Calculates and ranks
documents by their cosine similarity scores to the queries. Stores results
in a text document.

"""
import numpy as np
import re
import json
import math
import operator

class cosineVSM():
    
    def __init__(self, parsedQueries, indexPath, outputPath, corpusPath):
        self.parsedQueries = parsedQueries
        self.index = np.load(indexPath).item()
        self.outputPath = outputPath
        self.corpusPath = corpusPath       
        
    def getLexicon(self, lexiconPath):
        self.lexicon = np.load(lexiconPath).item()

    #--------------------------------------------------------------------------     
    #                        Retrieval Function 
    #--------------------------------------------------------------------------            
    def retrieve(self):
        print("\nOutputting ranked retrievals to: " + self.outputPath + "\n")
        outputFile = open(self.outputPath, 'w')
        
        for query in self.parsedQueries:
            #Dictionary to store document scores
            docScores = dict()
            
            #List to rank scores
            docRankings = []
            
            #Regular expressions to extract IDs from our parsed documents
            #Putting doc IDs in a dictionary to associate with their scores
            docIDExtract = re.compile("FR[0-9]{6}-[0-9]-[0-9]{5}")
            parsedDocs = open(self.corpusPath)
            numDocs = 0
            for document in parsedDocs:
                docId = docIDExtract.findall(document)
                docIdStr = ''.join(docId)
                docScores[docIdStr] = {'numerator': 0, 'denomOne': 0,
                                       'denomTwo': 0, 'finalScore': 0}
                numDocs += 1            
            
            #Temporarily store each query in a dictionary
            #to later access term frequencies
            queryNo = 0
            tempQueryDict = dict()
            for i, token in enumerate(query.split()):
                #Get the query number
                if i == 0:
                    queryNo = str(query.split()[0])
                #Count up query term frequencies using a dictionary
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
                
                #If the term is not in the lexicon, then the Df will be 0 and 
                #score will not be affected
                if term not in self.lexicon:
                    termDf = 0
                else:
                    #If it's in the lexicon, get the termID and find term Df
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
            
            #After getting query term frequencies
            #For each term in dictionary, get the postings list in the index
            for term in tempQueryDict:
                
                #Components of our tf-idf scores
                queryTf = tempQueryDict[term]
                termDf = 0
                termIdf = 0                

                
                #If the term is not in the lexicon, then the Df will be 0 
                #and score will not be affected
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
                rankingString = (str(queryNo) + " " + document + " " +
                                str(docScores[document]['finalScore'])) 
                #Append to array
                docRankings.append(rankingString)
                
            #Sort the array
                docRankings.sort(key=lambda line: float(line.split()[2]),
                                 reverse = True)
            
            topHundred = docRankings[:100]            
            
            
            for i, result in enumerate(topHundred):
                resultString = topHundred[i]
                toWrite = (resultString.split()[0] + " 0 " + 
                           resultString.split()[1] + " " + str(i) + " " +
                           resultString.split()[2] + " COSINE")
                outputFile.write(toWrite + "\n")

        