# -*- coding: utf-8 -*-

"""
Created on Mon Sep 26 00:16:32 2016

@author: jerry
"""

class Query:
    'Base class for the query terms'
    
    def __init__(self, number, title):
        self.number = number
        self.title = title
        
    def printTitle(self):
        print(self.title)
        
        