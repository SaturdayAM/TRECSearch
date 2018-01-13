# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:28:32 2016

@author: jerry
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
        print("Getting lexicon from: " + lexiconPath)
        self.lexicon = np.load(lexiconPath).item()
            
        #Regex to extracts the tokens of the documents
        #Referenced:
        #   http://stackoverflow.com/questions/2403122/regular-expression-to-extract-text-between-square-brackets
#        docTokenExtract = re.compile("(?<=\[).+?(?=\])")
#        
#        for document in parsedDocs:
#            docTokens = docTokenExtract.findall(document)
#            tokenString = ''.join(docTokens)
#            tokenList = tokenString.split()
#            for token in tokenList:
#                print(token)
    def retrieve(self):
        print("\nOutputting ranked retrievals to: " + self.outputPath + "\n")
        
        outputFile = open(self.outputPath, 'w')
    
        
            
        #For each query in our parsed queries
        for query in self.parsedQueries:
#            print("Retrieving for query: \n")
#            print(query)
            
            #Use dictionary to store document scores
            docScores = dict()
            
            #Use list to rank the scores
            docRankings = []
            
            #Regular expressions to extract IDs from our parsed documents
            #Putting document IDs in a dictionary to associate with their scores
            docIDExtract = re.compile("FR[0-9]{6}-[0-9]-[0-9]{5}")
            parsedDocs = open(self.corpusPath)
            numDocs = 0
            for document in parsedDocs:
                docId = docIDExtract.findall(document)
                docIdStr = ''.join(docId)
                #Initialize all scores to 0: numerator, denominator part 1, denominator part 2
                docScores[docIdStr] = {'numerator': 0, 'denomOne': 0, 'denomTwo': 0, 'finalScore': 0}
                numDocs += 1            
            
            
            #Temporarily store each query in a dictionary
            #allows for easier access to term frequencies
            queryNo = 0
            tempQueryDict = dict()
            for i, token in enumerate(query.split()):
                #Get the query number
                if i == 0:
                    queryNo = str(query.split()[0])
#                    print("Query Number: " + " " + queryNo)
                #Count up query term frequencies using a dictionary
                else:
                    term = query.split()[i]
#                    print("Term: " + " " + term)
#                    termId = self.lexicon[term]
                    #Case: term is not in the dictionary
                    if term not in tempQueryDict:
                        tempQueryDict[term] = 1
                    #Case: term occurs more than once
                    else:
                        tempQueryDict[term] += 1
            
#            print("Calculating denominator query score: ")
            queryDenomScore = 0;
            #Calculating denominator score portion for query 
            for term in tempQueryDict:
                #Components of our tf-idf scores
                queryTf = tempQueryDict[term]
                #print("query.termfrequency: " + str(queryTf))
                termDf = 0
                termIdf = 0                

                
                #If the term is not in the lexicon, then the Df will be 0 and score
                #will not be affected
                if term not in self.lexicon:
                    termDf = 0
                else:
                    #It is in lexicon, need to get the termID and find term Df
                    termId = str(self.lexicon[term])
#                    print("Term: " + term)
                    
                    #use termID to get postings list.
                    #For each document key in the postings list
                    for document in self.index[termId]:
                        #iterate termDf
                        termDf += 1
                    #Repeat, now calculating the scores for each document
                    #In the postings list
                    
                    #Calculate idf for the term
                    #Looked up log function from:
                        #   https://docs.python.org/2/library/math.html
#                    print("termDf: " + str(termDf))
                    if termDf == 0:
                        termIdf = 0
                    else:
                        termIdf = math.log10(numDocs/termDf)
                    
#                    print("\nIDF of term: " + str(termIdf))
#                    print("\n")
            
                queryDenomScore += (queryTf*termIdf)
            
            queryDenomScore = queryDenomScore**2
            
            #After getting query term frequencies
#            print(str(queryNo) + "|" + json.dumps(tempQueryDict))
            #For each term in the dictionary, get the postings list in the index
#            print("Calculating doc scores:\n")
            for term in tempQueryDict:
                #print("\nFor: " + term)
                
                #Components of our tf-idf scores
                queryTf = tempQueryDict[term]
                #print("query.termfrequency: " + str(queryTf))
                termDf = 0
                termIdf = 0                

                
                #If the term is not in the lexicon, then the Df will be 0 and score
                #will not be affected
                if term not in self.lexicon:
                    termDf = 0
                else:
                    #It is in lexicon, need to get the termID and find term Df
                    termId = str(self.lexicon[term])
#                    print("Term: " + term)
                    
                    #use termID to get postings list.
                    #For each document key in the postings list
                    for document in self.index[termId]:
                        #iterate termDf
                        termDf += 1
                    #Repeat, now calculating the scores for each document
                    #In the postings list
                    
                    #Calculate idf for the term
                    #Looked up log function from:
                        #   https://docs.python.org/2/library/math.html
#                    print("termDf: " + str(termDf))
                    if termDf == 0:
                        termIdf = 0
                    else:
                        termIdf = math.log10(numDocs/termDf)
                    
#                    print("\nIDF of term: " + str(termIdf))
#                    print("\n")
                    
                    for document in self.index[termId]:
#                        if document == "FR940810-0-00143":
#                            print("Document: FR940810-0-00143")
                        
                        #print("Document: " + document)                        
                        docTf = self.index[termId][document]
#                        if document ==  "FR940810-0-00143":
#                            print("DocTf: " + str(docTf))
                                                
                              
                        #print("Tf: " + str(docTf) + "\n")
                        numerator = (queryTf*termIdf)*(docTf*termIdf)
                        denomPartOne = (docTf*termIdf)**2
                        
                        #update the relevant components of cosineVSM in the scores dictionary
                        
#                        if document ==  "FR940810-0-00143": 
#                            print("Updating numerator by: " + str(numerator))
#                            print("Updating denomOne by: " + str(denomPartOne))
#                            print("Updating denomTwo by: " + str(queryDenomScore))
                        
                        
                        docScores[document]['numerator'] += numerator
                        docScores[document]['denomOne'] += denomPartOne
                        docScores[document]['denomTwo'] = queryDenomScore

            for document in docScores:
                #looked up sqrt() from:
                #   https://www.tutorialspoint.com/python/number_sqrt.htm
                numerator = docScores[document]['numerator']
                denomOne = docScores[document]['denomOne']
                denomTwo = docScores[document]['denomTwo']
                denominator = math.sqrt(denomOne+denomTwo)
                
                
                if denominator == 0:
                    finalScore = 0
                else:
                    finalScore = numerator/denominator
                docScores[document]['finalScore'] = finalScore
                
#            print("Final score for  FR940810-0-00143: " + str(docScores["FR940810-0-00143"]['finalScore']))
#            print("Numerator for  FR940810-0-00143: " + str(docScores["FR940810-0-00143"]['numerator']))
#            print("denomOne for  FR940810-0-00143: " + str(docScores["FR940810-0-00143"]['denomOne']))
#            print("denomTwo for  FR940810-0-00143: " + str(docScores["FR940810-0-00143"]['denomTwo']))
#            
#            print("Final score for  FR940617-2-00227: " + str(docScores["FR940617-2-00227"]['finalScore']))
            
            #Now, for each given query, we need to get the top 100 results
            #First, add the documents with their scores into our array
            for document in docScores:
                #Create string with the query number, document number, and the score
                rankingString = str(queryNo) + " " + document + " " + str(docScores[document]['finalScore']) 
                #Append to array
                docRankings.append(rankingString)
                
            #Sort the array
                docRankings.sort(key=lambda line: float(line.split()[2]), reverse = True)
            
            topHundred = docRankings[:100]            
            
            
            for i, result in enumerate(topHundred):
                resultString = topHundred[i]
                toWrite = resultString.split()[0] + " 0 " + resultString.split()[1] + " " + str(i) + " " + resultString.split()[2] + " COSINE"
                outputFile.write(toWrite + "\n")

        