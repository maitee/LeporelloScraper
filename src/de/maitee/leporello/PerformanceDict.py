'''
Created on Feb 27, 2012

@author: kms
'''

class Performance(dict):
    '''
    classdocs
    '''


    def __init__(self, date=None, location=None):
        '''
        Constructor
        '''
        dict.__init__({})
        self.date = date
        self.location = location
        
        self.type = None
        self.cast = dict()
        
        self.performance_detail_soup = None
        
    # addMemberToCast
    
    
#    def setPerformanceDetails(self, soup):