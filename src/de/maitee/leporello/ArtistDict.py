# coding: utf-8

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
from LeporelloDict import Leporello
from LeporelloAssistant import Lepistant


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
    def _addRole(self, role):
        if role:
            if role in PlayDict.PRODUCERS_CAST and not role in self.producer_roles:
                self.producer_roles.append(role)
                logger.info('%s - added new role "%s" to producer_roles.', self.full_name, role)
            else:
                if role not in self.artist_roles:
                    self.artist_roles.append(role)
                    logger.info('%s - added new role "%s" to artist_roles.', self.full_name, role)
    
    def _setData(self, data_list):
        role = None
        full_name = ''
        url = Lepistant.NOT_AVAILABLE
        
        for element in data_list:
            if 'class="eventDetailPerson"' in str(element):
                full_name = element.string
            elif 'class="eventDetailPersonRole"' in str(element):
                try:
                    role = element.string.split(':')[0]
                except:
                    logger.info('Setting role to "%s" since no role could be find in data_list: %s', role, data_list)
            elif 'class="eventDetailPersonLink"' in str(element):
                full_name = element.string
                url = Lepistant.URL_PREFIX + re.search('href=\"(.+?)\"', str(element)).group(1)
        
        # Check if artist already exists.
        if full_name in Leporello.artists:
            artist = Leporello.artists[full_name]
            self.full_name = artist.full_name
            self.first_name = artist.first_name
            self.middle_name = artist.middle_name
            self.last_name = artist.last_name
            self.producer_roles = artist.producer_roles
            self.artist_roles = artist.artist_roles
            self.photo = artist.photo
            self.biography = artist.biography
            self.appearances = artist.appearances
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
        Leporello.artists[self.full_name] = self
        
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