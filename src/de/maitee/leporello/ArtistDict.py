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
        self.artist_item_soup = self._setDetails(artist_item_soup)
        self.full_name = self._setName(name)
        self.first_name = str()
        self.middle_name = str()
        self.last_name = str()
        
        self.photo = None
        self.biography = None
        self.appearances = None
        
        
        # 'Private' methods:
        def _setName(self, name):
            # TODO:
            
            return name
        
        def _setPhoto(self):
            # TODO:
            
            self.photo = ''
        
        def _setBiography(self):
            # TODO:
            
            self.biography = ''
            
        def _setAppearances(self):
            # TODO:
            
            self.appearances = list()
        
        def _setDetails(self, soup):
            self._setPhoto()
            self._setBiography()
            self._setAppearances()
            
            return soup