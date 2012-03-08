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
            logger.info('%s - added "%s" to producer_roles.', self.full_name, role)
        else:
            self.artist_roles.append(role)
            logger.info('%s - added "%s" to artist_roles.', self.full_name, role)
    
    def _setData(self, data_list):
        role = Lepistant.NOT_AVAILABLE
        full_name = ''
        url = Lepistant.NOT_AVAILABLE
        
        for element in data_list:
            if 'class="eventDetailPerson"' in str(element):
                full_name = element.string
            elif 'class="eventDetailPersonRole"' in str(element):
                try:
                    role = element.string.split(':')[0]
                except:
                    logger.warning('%s - set role to "%s" since no role could be find in data_list: %s', role, data_list)
            elif 'class="eventDetailPersonLink"' in str(element):
                full_name = element.string
                url = Lepistant.URL_PREFIX + re.search('href=\"(.+?)\"', str(element)).group(1)
        
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
                logger.info('%s - set full_name, middle_name and last_name to "%s", "%s" and "%s".', 
                            self.full_name, self.first_name, self.middle_name, self.last_name)
            else:
                logger.info('%s - set full_name and last_name to "%s" and "%s".', self.full_name, self.first_name, self.last_name)
    
    def _setPhoto(self, soup):
        img_tag = soup.find('img', {"class": "person-picture"})
        url = Lepistant.getURLFromImageTag(img_tag)
        if url:
            self.photo = url
        else:
            self.photo = Lepistant.NOT_AVAILABLE
            
        logger.info('%s - set photo: "%s".', self.full_name, self.photo)
    
    def _setBiography(self, soup):
        biography_p_tag = soup.findAll('p', {"class": "person-description"})
        biography = Lepistant.formatParagraphsToString(biography_p_tag)
#        print repr(biography)
        if biography:
            self.biography = biography
        else:
            self.biography = Lepistant.NOT_AVAILABLE
            
        logger.info('%s - set biography: "%s...".', self.full_name, repr(self.biography[:Lepistant.LOG_MESSAGE_LENGTH]))
        
    def _setAppearances(self, soup):
        appearances = []
        try:
            appearance_ul_tag = soup.findAll('ul', {"class": "events"})[0]
            appearance_link_tags = appearance_ul_tag.findAll('a')
            for link in appearance_link_tags:
                appearances.append(link.string)
            self.appearances = appearances
            logger.info('%s - set appearances: "%s".', self.full_name, self.appearances)
        except:
            logger.warning('Failed to set appearances for artist "%s". Therefore setting appearances to an empty list',self.full_name)
    
    def _setDetails(self, soup):
        if soup:
            self._setPhoto(soup)
            self._setBiography(soup)
            self._setAppearances(soup)
        
        return soup