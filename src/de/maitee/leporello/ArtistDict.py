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
        self.first_name = str()
        self.middle_name = str()
        self.last_name = str()
        self.full_name = self._setName(name)
        
        self.photo = None
        self.biography = None
        self.appearances = None
        self.artist_item_soup = self._setDetails(artist_item_soup)
        
        
    # 'Private' methods:
    def _setName(self, name):
        splitted_name = name.split(' ')
        self.first_name = splitted_name[0]
        if len(splitted_name) > 1:
            self.last_name = splitted_name[-1]
            if len(splitted_name) > 2:
                self.middle_name = ''
                seq = splitted_name[1:-1]
                for element in enumerate(seq):
                    self.middle_name += element[1]
                    if element[1] != seq[-1]:
                        self.middle_name += ' '
#                print('in _setName(' + self.first_name + ' ' + self.middle_name + ' ' + self.last_name + ')')
            else:
#                print('in _setName(' + self.first_name + self.last_name + ')')
                pass
        
        return name
    
    def _setPhoto(self):
        # TODO:
        photos = []
        img_tag = self.artist_item_soup.find('img', {"class": "person-picture"})
        print img_tag
        print('in _setPhotos(' + str(photos) + ')')
        
        self.photo = ''
    
    def _setBiography(self):
        # TODO:
        biography = ''
        print('in _setBiography(' + biography + ')')
        
        self.biography = ''
        
    def _setAppearances(self):
        # TODO:
        appearances = []
        print('in _setAppearances(' + str(appearances) + ')')
        
        self.appearances = list()
    
    def _setDetails(self, soup):
        if soup:
            self._setPhoto()
            self._setBiography()
            self._setAppearances()
        
        return soup