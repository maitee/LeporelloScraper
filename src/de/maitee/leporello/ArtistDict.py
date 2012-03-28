# coding: utf-8

'''
Created on Mar 5, 2012

@author: simon
'''

# Standard libraries
import re
import logging
# Local libraries
#from LeporelloScraper import leporello
from LeporelloAssistant import Lepistant
from LeporelloAssistant import leporello
import PlayDict


logger = logging.getLogger('leporello')


class Artist(dict):
    '''
    classdocs
    '''


    def __init__(self, data_list):
        '''
        Constructor
        @param data_list: A list in a form of "[<span class="eventDetailPersonRole">Regie:&nbsp;</span>, 
                                                <a href="/de_DE/person/59253" class="eventDetailPersonLink" title="Volker L�sch">Volker L�sch</a>]".
        '''
        dict.__init__(self, {})
        
        self.full_name = str()
        self.first_name = str()
        self.middle_name = str()
        self.last_name = str()
        
        self.artist_roles = list()
        self.producer_roles = list()
        
        self.photo = str()
        self.biography = str()
        self.appearances = list()
        
        self.soup_details = None
        self.data_list = self._setData(data_list)
        
    # 'Private' methods:
    def _setKey(self, key, value):
        self[key] = value
        
        return value
    
    def _addRole(self, role):
        if role:
            if (role in PlayDict.PRODUCERS_CAST) and (role not in self.producer_roles):
                self.producer_roles.append(role)
                self._setKey('producer_roles', self.producer_roles)
                logger.info('%s - added new role "%s" to producer_roles.', self.full_name, role)
            else:
                if role not in self.artist_roles:
                    self.artist_roles.append(role)
                    self._setKey('artist_roles', self.artist_roles)
                    logger.info('%s - added new role "%s" to artist_roles.', self.full_name, role)
        
    
    def _setData(self, data_list):
        role = None
        full_name = ''
        url = Lepistant.NOT_AVAILABLE
        
        for element in data_list:
            if 'class="eventDetailPerson"' in str(element):
                full_name = element.string.lstrip().rstrip()
            elif 'class="eventDetailPersonRole"' in str(element):
                try:
                    role = element.string.split(':')[0].lstrip().rstrip()
                except:
                    logger.info('Setting role to "%s" since no role could be find in data_list: %s', role, data_list)
            elif 'class="eventDetailPersonLink"' in str(element):
                full_name = element.string.lstrip().rstrip()
                url = Lepistant.URL_PREFIX + re.search('href=\"(.+?)\"', str(element)).group(1)
        
        # Check if artist already exists.
        if full_name in leporello.artists:
            artist = leporello.artists[full_name]
            self.full_name = self._setKey('full_name', artist.full_name)
            self.first_name = self._setKey('first_name', artist.first_name)
            self.middle_name = self._setKey('middle_name', artist.middle_name)
            self.last_name = self._setKey('last_name', artist.last_name)
            self.producer_roles = self._setKey('producer_roles', artist.producer_roles)
            self.artist_roles = self._setKey('artist_roles', artist.artist_roles)
            self.photo = self._setKey('photo', artist.photo)
            self.biography = self._setKey('biography', artist.biography)
            self.appearances = self._setKey('appearances', artist.appearances)
        else:
            self._setName(full_name)
            if url:
                file_path = Lepistant.createFilePath(Lepistant.REL_PATH_ARTISTS_FOLDER, full_name, 'html')
                soup = Lepistant.getSoup(url, file_path)
                self._setDetails(soup)
            
        if role:
            self._addRole(role)
            
        # Add artist to the leporello artists dictionary so we can check later if the artist already exists.
        # If the artist exists we only update his data.
        leporello.artists[self.full_name] = self
        
        return data_list
    
    def _setName(self, name):
        self.full_name = self._setKey('full_name', name)
        
        splitted_name = name.split(' ')
        self.first_name = splitted_name[0]
        
        if len(splitted_name) > 1:
            self.last_name = self._setKey('last_name', splitted_name[-1])
            
            if len(splitted_name) > 2:
                middle_name = ''
                seq = splitted_name[1:-1]
                
                for element in enumerate(seq):
                    middle_name += element[1]
                    if element[1] != seq[-1]:
                        middle_name += ' '
                
                self.middle_name = self._setKey('middle_name', middle_name)
                logger.info('%s - set full_name, middle_name and last_name to "%s", "%s" and "%s".', 
                            self.full_name, self.first_name, self.middle_name, self.last_name)
            else:
                logger.info('%s - set full_name and last_name to "%s" and "%s".', self.full_name, self.first_name, self.last_name)
    
    def _setPhoto(self, soup):
        img_tag = soup.find('img', {"class": "person-picture"})
        url = Lepistant.getURLFromImageTag(img_tag)
        
        if url:
            photo = url
        else:
            photo = Lepistant.NOT_AVAILABLE
        
        self.photo = self._setKey('photo', photo)
        logger.info('%s - set photo: "%s".', self.full_name, self.photo)
    
    def _setBiography(self, soup):
        biography_p_tag = soup.findAll('p', {"class": "person-description"})
        biography = Lepistant.formatParagraphsToString(biography_p_tag)
        
        if biography:
            biography = biography
        else:
            biography = Lepistant.NOT_AVAILABLE
        
        self.biography = self._setKey('biography', biography)
        logger.info('%s - set biography: "%s...".', self.full_name, repr(self.biography[:Lepistant.LOG_MESSAGE_LENGTH]))
        
    def _setAppearances(self, soup):
        appearances = []
        
        try:
            appearance_ul_tag = soup.findAll('ul', {"class": "events"})[0]
            appearance_link_tags = appearance_ul_tag.findAll('a')
            
            for link in appearance_link_tags:
                appearances.append(link.string)

            self.appearances = self._setKey('appearances', appearances)
            logger.info('%s - set appearances: "%s".', self.full_name, self.appearances)
        except:
            logger.warning('Failed to set appearances for artist "%s". Therefore setting appearances to an empty list',self.full_name)
    
    def _setDetails(self, soup):
        if soup:
            self._setPhoto(soup)
            self._setBiography(soup)
            self._setAppearances(soup)
        
        return soup