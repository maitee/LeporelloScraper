'''
Created on Mar 5, 2012

@author: simon
'''

# Standard libraries
import re
import logging
from itertools import groupby
# Local libraries
import PlayDict
from LeporelloAssistant import Lepistant


logger = logging.getLogger('leporello')


class Artist(dict):
    '''
    classdocs
    '''


    def __init__(self, data_list):
        '''
        Constructor
        '''
        dict.__init__({})
        
        self.full_name = str()
        self.first_name = str()
        self.middle_name = str()
        self.last_name = str()
        
        self.artist_roles = list()
        self.producer_roles = list()
        
        self.photo = None
        self.biography = None
        self.appearances = None
        self.soup_details = None
        
        self.data_list = self._setData(data_list)
        
    # 'Private' methods:
    def _setRole(self, role):
        if role and role in PlayDict.PRODUCERS_CAST:
            self.producer_roles.append(role)
        else:
            self.artist_roles.append(role)
    
    
    def _setData(self, data_list):
        print('>>>>>>>>>> in ArtistDict._setData() <<<<<<<<<<')
        
        role = ''
        full_name = ''
        url = ''
        
        for element in data_list:
            if 'class="eventDetailPersonRole"' in str(element):
                try:
                    role = element.string.split(':')[0]
                except:
                    print('>>>>>>>>>> Could not extract a role from "' + str(data_list) + '" due to missing ":". ' + 
                          'This probably means that this data_list does not have a role')
            elif 'class="eventDetailPersonLink"' in str(element):
                full_name = element.string
                url = Lepistant.URL_PREFIX + re.search('href=\"(.+?)\"', str(element)).group(1)
            elif 'class="eventDetailPerson"' in str(element):
                full_name = element.string
        
        self._setName(full_name)
        if role:
            self._setRole(role)
        if url:
            file_path = Lepistant.createFilePath(Lepistant.REL_PATH_ARTISTS_FOLDER, full_name, 'html')
            soup = Lepistant.getSoup(url, file_path)
            self._setDetails(soup)
            
        return data_list
    
    def _setName(self, name):
        self.full_name = name
        
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