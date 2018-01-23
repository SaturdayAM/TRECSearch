# -*- coding: utf-8 -*-
"""
Parses the provided TREC query files.

"""
import numpy as np
import re
import mmap

class queryParser():
    
    def __init__(self, queryPath):
        self.queryPath = queryPath
        
        
        
    def parseQuery(self):
        queryFile = open(self.queryPath, "r")
        queryFileText = queryFile.read()
        wholeQueryPattern = re.compile("(?s)<top>(.*?)<\/top>")
        self.queryArray = []
        self.queryNumbers = []        
        self.specialTokens = []        
        
        #Putting all queries into an array
        allQueries = re.findall(wholeQueryPattern, queryFileText)
         
        for i, aQuery in enumerate(allQueries):
            newString = ''.join(allQueries[i])
            self.queryArray.append(newString)            
            
        
        #Removing all the tags from the query
        queryNoPattern = re.compile("<num> Number: [0-9]+")
        topicTag = re.compile("<title> Topic: ")
        descTag = re.compile("<desc> Description: ")
        narrTag = re.compile("<narr> Narrative: ")
        queryTitlePattern = re.compile("<title> Topic: (.*?)\n")
        for i, query in enumerate(self.queryArray):
            numberMatch = queryNoPattern.findall(self.queryArray[i])
            queryNumberStr = ''.join(numberMatch)
            numberOnly = re.findall("[0-9]+", queryNumberStr)
            numberOnlyStr = ''.join(numberOnly)
            
            #Getting the respective query numbers
            self.queryNumbers.append(numberOnlyStr)            
            
            queryTitle = queryTitlePattern.findall(self.queryArray[i])
            queryTitleStr = ''.join(queryTitle)
            
            self.queryArray[i] = queryTitleStr
            
            
        
        #Removing symbols
        symbolPattern = re.compile("[^\w]")            
        for i, query in enumerate (self.queryArray):
            symboless = symbolPattern.sub(' ', self.queryArray[i])
            self.queryArray[i] = symboless
            
        #Case folding
        for i, query in enumerate(self.queryArray):
            lowerCaseStr = self.queryArray[i].lower()
            lowerCaseStr.strip()
            self.queryArray[i] = lowerCaseStr
            
        #Creating our final parsed queries list
        self.parsedQueries = []
        for i, query in enumerate(self.queryArray):
            strToAdd = self.queryNumbers[i] + " " + self.queryArray[i]
            self.parsedQueries.append(strToAdd)
        
        
        self.longQueries = []
            