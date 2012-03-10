# coding: utf-8

'''
Created on Mar 10, 2012

@author: simon
'''

import logging


logger = logging.getLogger('leporello')


class Borg(dict):
    _shared_state = {}
    def __init__(self):
        dict.__init__({})
        self.__dict__ = self._shared_state


class Leporello(Borg):
    '''
    classdocs
    '''
    plays = list()
    artists = dict()
    
#    def __init__(self):
#        '''
#        Constructor
#        '''
##        Borg.__init__(self)
#        dict.__init__({})
        


#def singleton(class_):    
#    instances = {}
#    def getInstance(*args, **kwargs):
#        if class_ not in instances:
#            instances[class_] = class_(*args, **kwargs)
#        
#        return instances[class_]
#    
#    return getInstance()
#
#@singleton
#class Leporello(dict):
#    '''
#    classdocs
#    '''
#        
#    plays = dict()
#    artists = dict()
    
    
#class Singleton(object):
#    _instance = None
#    def __new__(cls, *args, **kwargs):
#        if not isinstance(cls._instance, cls):
#            cls._instance = dict.__new__(cls, *args, **kwargs)
#        
#        return cls._instance
#    
#class Leporello(Singleton, dict):
#    plays = dict()
#    artists = dict()