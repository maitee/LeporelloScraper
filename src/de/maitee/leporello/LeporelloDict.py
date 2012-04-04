# coding: utf-8

'''
Created on Mar 10, 2012

@author: simon
'''

import logging


logger = logging.getLogger('leporello')


#class Borg(dict):
#    _shared_state = {}
#    def __init__(self):
#        dict.__init__({})
#        self.__dict__ = self._shared_state


class Leporello(dict):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        dict.__init__({})
        
        self.theatre = self._setKey('theatre', 'Theater Bremen')
        self.season = self._setKey('season', '2011/2012')
        self.website = self._setKey('website', 'http://www.theaterbremen.de/de_DE/home')
        self.box_office = self._setKey('box_office', '04213653333')
        self.email = self._setKey('email', 'service@theaterbremen.de')
        self.plays = self._setKey('plays', list())
        
        self.straight_theater = self._setKey('straight_theater', list())
        self.musical_theater = self._setKey('musical_theater', list())
        self.dance_theater = self._setKey('dance_theater', list())
        self.moks = self._setKey('moks', list())
        self.junge_akteure = self._setKey('junge_akteure', list())
        
        self.artists = self._setKey('artists', dict())
        self.leporello_info = dict()
    
    
    def _setKey(self, key, value):
        self[key] = value
        
        return value