'''
Created on Mar 5, 2012

@author: simon
'''

class Artist(dict):
    '''
    classdocs
    '''


    def __init__(self, artist_item_soup, name):
        '''
        Constructor
        '''
        dict.__init__({})
        self.artist_item_soup = artist_item_soup
        self.name = self._setName(name)
        self.first_name = str()
        self.middle_name = str()
        self.last_name = str()
        
        self.photo = None
        self.biography = None
        self.appearances = None
        
        
        # 'Private' methods:
        def _setName(self, name):
            # TODO:
#            name = 'name'
            print('in _setName(' + name + ')')
            
            return name
        
        def _setPhoto(self):
            # TODO:
            print('in _setName(' + [] + ')')
            
            self.photo = ''
        
        def _setBiography(self):
            # TODO:
            print('in _setName(' + '' + ')')
            
            self.biography = ''
            
        def _setAppearances(self):
            # TODO:
            print('in _setName(' + [] + ')')
            
            self.appearances = list()
        
        def _setDetails(self, soup):
            self._setPhoto()
            self._setBiography()
            self._setAppearances()
            
            return soup