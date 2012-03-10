'''
Created on Mar 10, 2012

@author: simon
'''

import logging


logger = logging.getLogger('leporello')


class Leporello(dict):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        dict.__init__({})
        
        self.plays = dict()
        self.artists = dict()
        