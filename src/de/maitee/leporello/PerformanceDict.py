'''
Created on Feb 27, 2012

@author: kms
'''

import logging
import datetime


logger = logging.getLogger('leporello')


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
        self.producers_cast = None
        
        self.soup = None
        
    
    # 'Private' methods:
    def _updateLocation(self, title):
        try:
            location_p_tag = self.soup.find('h3', text=title).parent.findNextSiblings('p')[1]
            location = location_p_tag.text
            self.location = location
            logger.info('Updated location to "%s" of performance.', self.location)
        except:
            logger.warning('Failed to update location. Keep default location: %s', self.location)
            
        logger.info('')
        
    def _setCast(self):
        pass
        
        
    # 'Public' methods:
    def setDetails(self, soup, title):
        self.soup = soup
        
        self._updateLocation(title)
        self._setCast()
    
    
    
#    def setPerformanceDetails(self, soup):