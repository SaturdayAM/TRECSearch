# -*- coding: utf-8 -*-

"""
Object to store queries

"""

class Query:
    'Base class for the query terms'
    
    def __init__(self, number, title):
        self.number = number
        self.title = title
        
    def printTitle(self):
        print(self.title)
        
        