# -*- coding: utf-8 -*-
import re

class docParser():
    """
    takes in the unconcactenated array of data files,
    separates them into individual documents,
    saves them as a (docNo, terms)
    
    """

    
    def __init__(self, unparsedPath):
        self.unparsedPath = unparsedPath
        self.subCorpus = []
        self.docNos = []
        self.docTexts = []
      
      
    
    #Go through all files, and parse each file as
    #(DocNO [Parsed Text])
    #Looked at regex for files in:
    #   http://stackoverflow.com/questions/10477294/how-do-i-search-for-a-pattern-within-a-text-file-using-python-combining-regex
    #   http://stackoverflow.com/questions/6434823/python-list-everything-between-two-tags
    #   https://regex101.com/
    #Looked at replacing regex matches at:
    #   https://en.wikibooks.org/wiki/Python_Programming/Regular_Expression#Replacing
    #Looked at removing whitespaces and newlines at:
    #   http://stackoverflow.com/questions/16566268/remove-all-line-breaks-from-a-long-string-of-text
    #Looked at case-folding at: 
    #   http://stackoverflow.com/questions/6797984/how-to-convert-string-to-lowercase-in-python
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
        #Iterate through matches to remove generic tags, e.g. <BILLING></BILLING>
        for i, documentTexts in enumerate(matches):
            newString = commentPattern.sub('', matches[i])
            newString = genericTagPattern.sub(' ', matches[i])
            newString = " ".join(newString.split())
            self.docTexts.append(newString)

        #Handling the SGML escape sequences
        
            
        #Handling special cases: USA, PHD, BS, MS
        #Handling special tokens: ^ * # @ $
        
        
        
        
        
        
        
        #Looked at file writing from:
        #   http://stackoverflow.com/questions/899103/writing-a-list-to-a-file-with-python
        with open(outputPath, 'w') as file_handler:
            for i in range(len(self.docTexts)):
                toWrite = "(" + self.docNos[i] + "[" + self.docTexts[i] + "])"
                file_handler.write('(' +self.docNos[i] + "[" + self.docTexts[i] + "])\n\n")
                self.subCorpus.append(toWrite)