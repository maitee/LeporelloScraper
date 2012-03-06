'''
Created on Mar 5, 2012

@author: simon
'''
from de.maitee.leporello.LeporelloAssistant import Lepistant

class Artist(dict):
    '''
    classdocs
    '''


    def __init__(self, soup, name):
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
        self.soup = self._setDetails(soup)
        
        
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
    
    def _setPhoto(self, soup):
        img_tag = soup.find('img', {"class": "person-picture"})
        url = Lepistant.getURLFromImageTag(img_tag)
        self.photo = url
    
    def _setBiography(self, soup):
        # TODO:
        biography_p_tag = soup.findAll('p', {"class": "person-description"})
        biography = Lepistant.formatParagraphsToString(biography_p_tag)
        print repr(biography)
        print biography
#        print('in _setBiography(' + biography + ')')
        
        self.biography = ''
        
    def _setAppearances(self, soup):
        # TODO:
        appearances = []
#        print('in _setAppearances(' + str(appearances) + ')')
        
        self.appearances = list()
    
    def _setDetails(self, soup):
        if soup:
            self._setPhoto(soup)
            self._setBiography(soup)
            self._setAppearances(soup)
        
        return soup