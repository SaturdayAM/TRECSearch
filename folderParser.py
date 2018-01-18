# -*- coding: utf-8 -*-
import re
import os
import datetime
import dateutil.parser as dateParser
import numpy as np
import json

class folderParser():
    """
    Parses all files in folder path and writes to disk a parsed corpus
    in the form: (DocNO [Parsed Tokens])
    
    """


    def __init__(self, folderPath, outputPath):
        self.outputPath = outputPath
        self.folderPath = folderPath
        self.docNos = []
        self.docTexts = []
        self.specialTokens = []
      
      
      
    #--------------------------------------------------------------------------     
    #                        Main Parse Function 
    #--------------------------------------------------------------------------
    def parse(self):
        #Regular expressions to extract tags
        docNoPattern = re.compile("<DOCNO>(.*?)<\/DOCNO>")
        commentPattern = re.compile("<!--.*-->")
        textPattern = re.compile("<TEXT>(.*?)<\/TEXT>", re.DOTALL)
        genericTagPattern = re.compile("<(.*?)>")
                
        for filename in os.listdir(self.folderPath):
            tempPath = self.folderPath + '/' + filename
            tempFile = open(tempPath, "r")
           
            #Getting all the document numbers from the folder
            for line in tempFile:
                    self.docNos += docNoPattern.findall(line) 
                    
            #Finding all the <TEXT></TEXT> blocks, store in matches
            tempFile.seek(0)
            textFile= tempFile.read()
            matches = re.findall(textPattern, textFile)
        
            #Iterate matches, remove comments, generic tags, and newlines
            #Append matches[i] to docTexts[i]
            for i, documentTexts in enumerate(matches):
                newString = commentPattern.sub('', matches[i])
                newString = genericTagPattern.sub(' ', matches[i])
                newString = " ".join(newString.split())
                self.docTexts.append(newString)
        
        
        #---------------------Parsing escape sequences-------------------------
        """
        Allows for more accurate handling of special case terms
        Escape sequence patterns
        """
        hyphens = re.compile("&hyph;")
        ampersands = re.compile("&amp;")
        sections = re.compile("&sect;")
        paragraphs = re.compile("&para;")
        toBeBlanks = re.compile("&[a-z]+;")
        for i, text in enumerate(self.docTexts):
            escapeless = self.docTexts[i]
            escapeless = hyphens.sub('-', escapeless)
            escapeless = ampersands.sub('&', escapeless)
            escapeless = sections.sub('\u00A7', escapeless)        
            escapeless = paragraphs.sub('\u00B6', escapeless)
            escapeless = toBeBlanks.sub(' ', escapeless)
            self.docTexts[i] = escapeless
            
            
        #--------------------------Handling numbers----------------------------
        """Regex patterns for numbers with comas, decimals"""

        numCommaPattern = re.compile("(\d),(\d)")
        redunDecPattern = re.compile("(\d)\.0+(?!\d)")
        for i, text in enumerate(self.docTexts):
            parsedNumStr = self.docTexts[i]
            parsedNumStr = numCommaPattern.sub(r"\1\2", parsedNumStr)
            parsedNumStr = redunDecPattern.sub(r"\1", parsedNumStr)
            self.docTexts[i] = parsedNumStr
        
        #------------------------Handling Special Tokens-----------------------
        """
        Handles various tokens that can be found from dates in the documents
        """
        fullDates = re.compile("(?:January|February|March|April|May|June|July"
            "|August|September|October|November|December)(?:\s+|$)[0-9]{1,2},"
            "(?:\s+|$)[0-9]{4}")

        slashDates = re.compile("\s([0-9][0-9]\/[0-9][0-9]\/[0-9]{2,4})")
        
        #Traverse each document's text; filter and store special tokens
        for i, document in enumerate(self.docTexts):        
            currentText = self.docTexts[i]
            completes = fullDates.findall(currentText) #Store the full dates
            slashes = slashDates.findall(currentText) #Store the slash dates
            dateCollection = completes + slashes #Aggregate for dates            
            
            currentText = fullDates.sub(' ', currentText) #Clean text            
            currentText = slashDates.sub(' ', currentText) #Clean text
            self.docTexts[i] = currentText
            
            #Process with dateutil module
            #Dates are in format MM/DD/YYYY
            specTokenString = " "
            if len(dateCollection) > 0:
                for i, entry in enumerate(dateCollection):
                    date = dateParser.parse(dateCollection[i])
                    date = date.strftime('%m/%d/%Y')
                    specTokenString+= date + " "
            
            self.specialTokens.append(specTokenString) 
    
            
        #Removing symbols after storing special tokens
        symbolPattern = re.compile("[^\w]")
        for i, text in enumerate(self.docTexts):
            symboless = symbolPattern.sub(' ', self.docTexts[i])
            self.docTexts[i] = symboless
        
        
        #add the special tokens back after removing symbols
        for i, text in enumerate(self.docTexts):
            appendTokenStr = self.specialTokens[i];
            self.docTexts[i] += appendTokenStr 
        
        #Performing case-folding after parsing
        for i, text in enumerate(self.docTexts):
            lowercaseStr = self.docTexts[i].lower()
            self.docTexts[i] = lowercaseStr
        
        
        
        
    #--------------------------------------------------------------------------   
    #                         Output Parsed Corpus 
    #--------------------------------------------------------------------------        
    def writeParsedDocs(self):
        print("\nWriting parsed docs to: ", self.outputPath, "\n")
        with open(self.outputPath, 'w') as file_handler:
            for i in range(len(self.docTexts)):
                toWrite = "(" + self.docNos[i] 
                          + "[" + self.docTexts[i] + "])\n"
                file_handler.write(toWrite)
            
           
           
    #--------------------------Constructs the Lexicon---------------------------

    """        
    #   Builds a lexicon containing all unique tokens and a counter value
    #   termID becomes token_countervalue
    #   used a python dictionary
    #   Refered to the following sources for dictionary functions/traversal:
    #       https://www.mkyong.com/python/python-how-to-loop-a-dictionary/
    #       http://stackoverflow.com/questions/3496518/python-using-a-dictionary-to-count-the-items-in-a-list
    #       http://stackoverflow.com/questions/14374568/counting-duplicate-words-in-python-the-fastest-way
    """
       
    def buildLexicon(self):       
        lexicon = dict()
        docFrequency = dict()        
        tokenIndexer = 0;              
        for document in self.docTexts:
            tokenList = document.split()
            for token in tokenList:
                if token not in lexicon:
                    lexicon[token] = tokenIndexer
                    tokenIndexer += 1
                docFrequency[token] = docFrequency.get(token, 0) + 1
                
                
        #Saving the lexicon using numpy
        #Looked up how to do so at: 
        #   http://stackoverflow.com/questions/19201290/how-to-save-a-dictionary-to-a-file-in-python
        print("Saving lexicon to: middleFiles/lexicon.npy")
        np.save("middleFiles/lexicon.npy", lexicon)         
        
        #Also saving lexicon to json
        #Looked up how to do so at:
        #   http://stackoverflow.com/questions/11026959/python-writing-dict-to-txt-file-and-reading-dict-from-txt-file
        json.dump(lexicon, open("middleFiles/lexicon.txt", 'w'))
        
        return lexicon
        
        
        
    def termFrequencies(self):
         self.docFrequency = dict()
         for document in self.docTexts:
            tokenList = document.split()
            for token in tokenList:
                self.docFrequency[token] = self.docFrequency.get(token, 0) + 1
                
                
        