'''
Created on Feb 27, 2012

@author: kms
'''

# Standard libraries
import re
import logging
import datetime
from itertools import groupby
# Local libraries
from LeporelloAssistant import Lepistant
from ArtistDict import Artist
import PlayDict


logger = logging.getLogger('leporello')


class Performance(dict):
    '''
    classdocs
    '''


    def __init__(self, date, location, cast):
        '''
        Constructor
        '''
        dict.__init__(self, {})
        
        self.date = self._setKey('date', date)
        self.cast = self._setKey('cast', cast)
        self.location = self._setKey('location', location)
        
        self.type = None
        self.producer_cast = None
        
        self.soup = None
   
    @classmethod
    def getRoleFromArtistItem(cls, artist_item):
        role = Lepistant.NOT_AVAILABLE
        
        for element in artist_item:
            if 'class="eventDetailPersonRole"' in str(element):
                try:
                    role = element.string.split(':')[0]
                except:
                    logger.info('Setting role to "%s" since no role could be find in data_list: %s', role, artist_item)
        
        return role    
    
    # 'Private' methods:
    def _setKey(self, key, value):
        self[key] = value
        
        return value
    
    def _updateLocation(self, title):
        try:
            location_p_tag = self.soup.find('h3', text=title).parent.findNextSiblings('p')[1]
            location = location_p_tag.text.lstrip().rstrip().replace_all('&nbsp;', '')
            self.location = self._setKey('location', location)
            logger.info('Updated location to "%s" of performance.', self.location)
        except:
            logger.warning('Failed to update location. Keep default location: %s', self.location)
            
        logger.info('')
        
    def _updateCast(self):
        updated_cast = dict()
        
        try:
            artist_item_tags = self.soup.findAll('h4', text=re.compile('Besetzung'))[0].parent.findNextSiblings(['span', 'a', 'br'])
            
            if artist_item_tags:
                date = self.date
                artist_items = [list(tag[1]) for tag in groupby(artist_item_tags, lambda tag: str(tag) == '<br />') if not tag[0]]
                
                for artist_item in artist_items:
                    artist = Artist(artist_item)
                    role = Performance.getRoleFromArtistItem(artist_item)
                
                    if role and role not in PlayDict.PRODUCERS_CAST:
                        artist_role = role
                    
                        if role == Lepistant.NOT_AVAILABLE:
                            artist_role = artist.full_name
                        
                        updated_cast[artist_role] = artist.full_name
                        logger.info('Updated performance from %s - added artist to cast: {"%s": "%s"}', date, artist_role, artist.full_name)
                
                self.cast = self._setKey('cast', updated_cast)
            else:
                logger.info('Performance from %s - performance does not have a cast. Therefore setting cast and to an empty dictionary.', date)
        except IndexError as ierr:
            logger.warning('Failed to set cast for performance from "%s" due to: %s.', date, str(ierr))
        except AttributeError as attrerr:
            logger.warning('Failed to set cast for performance from "%s" due to: %s.', date, str(attrerr))
        
    # 'Public' methods:
    
    def setDetails(self, soup, title):
        self.soup = soup
        
        self._updateLocation(title)
        self._updateCast()
    
    
    
#    def setPerformanceDetails(self, soup):