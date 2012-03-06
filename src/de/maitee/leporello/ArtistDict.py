'''
Created on Mar 5, 2012

@author: simon
'''
from LeporelloAssistant import Lepistant

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
        if url:
            self.photo = url
        else:
            self.photo = Lepistant.NOT_AVAILABLE
    
    def _setBiography(self, soup):
        biography_p_tag = soup.findAll('p', {"class": "person-description"})
        biography = Lepistant.formatParagraphsToString(biography_p_tag)
#        print repr(biography)
        if biography:
            self.biography = biography
        else:
            self.biography = Lepistant.NOT_AVAILABLE
        
    def _setAppearances(self, soup):
        appearances = []
        try:
            appearance_ul_tag = soup.findAll('ul', {"class": "events"})[0]
            appearance_link_tags = appearance_ul_tag.findAll('a')
            for link in appearance_link_tags:
                appearances.append(link.string)
            self.appearances = appearances
        except:
            print('>>>>>>>>>> Could not set appearances due to: Appearances do not exist')
            self.appearances = Lepistant.NOT_AVAILABLE
        print self.appearances
    
    def _setDetails(self, soup):
        if soup:
            self._setPhoto(soup)
            self._setBiography(soup)
            self._setAppearances(soup)
        
        return soup