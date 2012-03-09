'''
Created on Feb 27, 2012

@author: kms
'''


import datetime


class Performance(dict):
    '''
    classdocs
    '''


    def __init__(self, date_time, location):
        '''
        Constructor
        '''
        dict.__init__({})
        
        self.date = date_time
        self.location = location
        
        self.type = None
        self.cast = dict()
        
        self.soup = None
        
        
    def setDetails(self, soup):
        self.soup = soup
        print('================ in PerformanceDict ==============')
    
    
    # 'Private' methods:
    
    
#    def setPerformanceDetails(self, soup):