# -*- coding: utf-8 -*-
"""
takes in the unconcactenated array of data files,
separates them into individual documents, saves them as a (docNo, terms)

"""
import re

class docParser():


    
    def __init__(self, unparsedPath):
        self.unparsedPath = unparsedPath
        self.subCorpus = []
        self.docNos = []
        self.docTexts = []
      
      
    
    #Go through all files, and parse each file as
    #(DocNO [Parsed Text])
    def parse(self, outputPath):
        #Begin with the filepath. Open multiple files
        unparsedFile = open(self.unparsedPath, "r")
        unparsedFile2 = open(self.unparsedPath, "r")
        unparsedFile3 = open(self.unparsedPath, "r")
        
        #Regular expressions to extract out of tags
        docNoPattern = re.compile("<DOCNO>(.*?)<\/DOCNO>")
        commentPattern = re.compile("<!--.*-->")
        textPattern = re.compile("<TEXT>(.*?)<\/TEXT>", re.DOTALL)
        genericTagPattern = re.compile("<(.*?)>")
        
        #Escape sequences
        hyphenSeq = re.compile("&hyph")
        blankSeq = re.compile("&blank")
        sectionSeq = re.compile("&sect")
        amperSand = re.compile("&amp")
        
        #Find all the document numbers, store in docNos[]
        for line in unparsedFile:
              self.docNos += docNoPattern.findall(line)
        print("Number of DocNo matches: ", len(self.docNos))
                
        #Finding all large <TEXT></TEXT> blocks, stores in matches
        textFile = unparsedFile3.read()
        matches = re.findall(textPattern, textFile)
        print("Number of text blocks: ", len(matches))
        
        #Go through matches, remove comment patterns and newlines
        #add each parsed element of matches[i] to docTexts[i]
        #Iterate through matches to remove generic tags
        for i, documentTexts in enumerate(matches):
            newString = commentPattern.sub('', matches[i])
            newString = genericTagPattern.sub(' ', matches[i])
            newString = " ".join(newString.split())
            self.docTexts.append(newString)

        with open(outputPath, 'w') as file_handler:
            for i in range(len(self.docTexts)):
                toWrite = "(" + self.docNos[i] + "[" + self.docTexts[i] + "])"
                file_handler.write('(' +self.docNos[i] + "[" + self.docTexts[i] + "])\n\n")
                self.subCorpus.append(toWrite)