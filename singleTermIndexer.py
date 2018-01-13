# -*- coding: utf-8 -*-
import folderParser
import os
import re
import tempfile
import json
import numpy as np

class singleTermIndexer():
    """
    takes a path to a folder, goes through each file in order
    to parse and then add the docNos and docTexts as it iterates.
    saves them as a (docNo, terms)
    
    """
    
    
    def __init__(self, dataPath, corpusPath, memory):
        self.dataPath = dataPath
        self.corpusPath = corpusPath
        self.memory = memory
    

    #------------------------Indexing Function---------------------------------
    #   1) Calls on doc parser to parse docs/build a lexicon
    #   2) Constructs a single term index
    #--------------------------------------------------------------------------    
    def buildIndex(self, unsortedTriplesPath, sortedTriplesPath, outputIndexPath):
        #Constructing lexicon
        fileParser = folderParser.folderParser(self.dataPath, self.corpusPath)
        fileParser.parse()
        fileParser.writeParsedDocs()
        self.lexicon = fileParser.buildLexicon()
                     
        #Regular expressions to extract IDs from our parsed documents
        docIDExtract = re.compile("FR[0-9]{6}-[0-9]-[0-9]{5}")
        #Pattern matches the tokens in the documents
        docTokenExtract = re.compile("(?<=\[).+?(?=\])")
        #Pattern matches term-ids in the triples lists
        tokenNoExtract = re.compile("(?<=_)[0-9]+")
        
        parsedDocs = open(self.corpusPath, "r")
        
        #------------Method to get term-ids from a triples list-----------------
        def sortTokenNo(triple):
            tokenNum  = tokenNoExtract.findall(triple)
            tokenNumStr = ''.join(tokenNum) 
            return int(tokenNumStr)
            
                            
        #Creates the unsorted, unmerged temporary triples lists
        #Goes through each document and each document's tokens
        #Writes lists to files while counting memory and number of files written
        memoryUsed = 0
        tempFileCount = 0 
        print("\nWriting unsorted/unmerged triples to: " + unsortedTriplesPath, "\n")
        
        tempFile = open(unsortedTriplesPath + "/tempTriples_0.txt", 'w')
        for document in parsedDocs:
             docID = docIDExtract.findall(document)
             docIdStr = ''.join(docID)
             docTokens = docTokenExtract.findall(document)
             tokenString = ''.join(docTokens)
             tokenList = tokenString.split()
             for token in tokenList:
                 tokenNo = self.lexicon[token]
                 triple = "( " + str(tokenNo) + " , " + docIdStr + " , 1 )"
                 memoryUsed += 1; 
                 if(memoryUsed <= 1000):
                     tempFile.write(triple + "\n")
                 else:
                     tempFileCount += 1;
                     tempFile = open(unsortedTriplesPath + "/tempTriples_" + str(tempFileCount) + ".txt", 'w')
                     tempFile.write(triple + "\n")
                     memoryUsed = 1;
        
        
        #Sorts the triples lists
        #Looked up python sorting/how to sort from a string from a file on:
        #   http://stackoverflow.com/questions/14591435/sorted-only-sorting-by-first-digit      
        #   http://stackoverflow.com/questions/3002392/blank-lines-in-file-after-sorting-content-of-a-text-file-in-python
        
        #Regular expression to match up the unsorted triple nos with the sorted
        unsortedFileNo = re.compile("[0-9]+")        
        print("\nWriting sorted triples lists to: " + sortedTriplesPath, "\n")
        
        for filename in os.listdir(unsortedTriplesPath):
            currentFileNo = unsortedFileNo.findall(filename)
            fileNoStr = ''.join(currentFileNo)
            currentFile = open(unsortedTriplesPath + '/' + filename, "r")
            lines = currentFile.readlines()
            lines.sort(key=lambda line: int(line.split()[1]))
            sortedFile = open(sortedTriplesPath + "/sortedTriples_" + fileNoStr + ".txt", 'w')
            sortedFile.writelines(lines)
            
                
        #Merging the sorted triples lists into our inverted index
        #Inverted index is stored as a dictionary where each key-value for
        #the terms is another dictionary with document frequencies 
        #Looked up using python dictionaries from:
        #   https://www.quora.com/In-Python-can-we-add-a-dictionary-inside-a-dictionary-If-yes-how-can-we-access-the-inner-dictionary-using-the-key-in-the-primary-dictionary
        self.invertedIndex = dict()
        print("\nWriting index to: " + outputIndexPath, "\n")
        
        for filename in os.listdir(sortedTriplesPath):
            tempPath = sortedTriplesPath + "/" + filename
            tempFile = open(tempPath, 'r')
            for line in tempFile:
                #Extract the relevant keys and values from the list
                termID = str(line.split()[1])
                docNo = str(line.split()[3])
                docTermFreq = str(line.split()[5])
                #Case 1: The term has not been added to index
                if termID not in self.invertedIndex:
                    secondaryDict = {}
                    secondaryDict[docNo] = 1
                    self.invertedIndex[termID] = secondaryDict
                    #Case 2: The term is in index, but the doc is not in the secondary dict
                elif docNo not in self.invertedIndex[termID]:
                    self.invertedIndex[termID][docNo] = 1
                #Case 3: term is in index, doc is in secondary dictionary
                else:
                    self.invertedIndex[termID][docNo] += 1
        
        #Outputting our inverted index
        #.txt file is so people can read the inverted index
        #.npy file used so the created index can be stored and used later
        #Looked up using JSON to output dictionaries at:
        #   http://stackoverflow.com/questions/26745519/converting-dictionary-to-json-in-python
        #   http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python
        #Looked up printing a dictionary with sorted keys at:
        #   http://stackoverflow.com/questions/4642501/how-to-sort-dictionaries-by-keys-in-python
        #   http://stackoverflow.com/questions/3426108/numeric-sort-in-python
        #Looke
        indexFile = open(outputIndexPath + "/singleTermIndex.txt", 'w')
        
        for term in sorted(self.invertedIndex, key = int):
            toWrite = json.dumps(term) + ": " + json.dumps(self.invertedIndex[term])+ "\n\n"
            indexFile.write(toWrite)
        
        #Looked up how to store dictionaries with numpy at:
        #   http://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file-in-python
        np.save(outputIndexPath + '/singleTermIndex.npy', self.invertedIndex)
        
        
    def displayLexicon(self):
        for token, value in self.lexicon.items():
            print(token, "--> ", value)
        print(len(self.lexicon))
    
    def calcFrequencies(self):
        for token, freq in self.docFrequency.items():
            print(token, "--> ", freq)
        print(len(self.docFrequency))
        