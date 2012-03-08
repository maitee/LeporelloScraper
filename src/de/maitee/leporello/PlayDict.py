# coding: utf-8

'''
Created on Feb 27, 2012

@author: kms
'''
# Standard libraries
import re
import logging
from itertools import groupby
# Local libraries
from LeporelloAssistant import Lepistant
from ArtistDict import Artist
from PerformanceDict import Performance


logger = logging.getLogger('leporello')


# Member names of producer's cast.
PRODUCERS_CAST = [
                  'Ausstattung', 
                  'Bühne', 
                  'Bühne + Kostüme', 
                  'Bühne und Kostüm', 
                  'Bühne und Kostüme', 
                  'Bühnenbild', 
                  'Chor', 
                  'Choreographie', 
                  'Chorleitung', 
                  'Dramaturgie', 
                  'Dramaturgie/Bearbeitung', 
                  'Grundgestaltung Brauhauskeller', 
                  'Inszenierung', 
                  'Inszenierung/ Choreographie/ Video', 
                  'Kinderchor', 
                  'Konzeption/ Inszenierung', 
                  'Konzeption/ Video', 
                  'Kostüm', 
                  'Kostüme', 
                  'Kostüme und Puppen', 
                  'Künstlerische Mitarbeit', 
                  'Musik', 
                  'Musikalische Leitung', 
                  'Opernchor + Extrachor Theater Bremen', 
                  'Puppentraining', 
                  'Regie', 
                  'Regie und Bühne', 
                  'Regie/ Bühne', 
                  'Regieassistenz', 
                  'Theaterpädagogik', 
                  'Video', 
                  'Videorealisation', 
                  'Visuelle Gestaltung', 
                  ]

class Play(dict, Lepistant):
    '''
    classdocs
    '''

    def __init__(self, play_item_soup):
        '''
        Constructor
        '''
        dict.__init__({})
        self.play_item_soup = play_item_soup
        self.title = self._setTitle()
        self.subtitle = self._setSubtitle()
        self.location = self._setLocation()
        self.dates = self._setDates()
        self.performances = self._setPerformances()

        self.link = str()
        self.file_name_on_disk = str()
        
        self.author = str()
        self.type = str()
        self.summary = str()
        self.further_info = str()
        self.critics = str()
        self.video = str()
        self.photos = list()
        self.cast = dict()
        self.sponsors = list()
        
        self.play_detail_soup = None
        
    # 'Private' methods:
    def _setDates(self):
        dates = list()
        try:
            dates_string = self.play_item_soup.findAll('p')[1].span.nextSibling
            # dates_string = "Neues Schauspielhaus / Termine: 10. | 14. | 18. September 2011, 01. | 16. | 22. Oktober 2011, 18. | 29. November 2011, 08. | 11. | 16. | 29. Dezember 2011, 27. Januar 2012, 03. | 10. | 15. | 26. Februar 2012, 27. März 2012"
            (location_part, seperator, dates_part) = dates_string.partition(':') 
            # dates_per_month = "[' 10. | 14. | 18. September 2011', ' 01. | 16. | 22. Oktober 2011', ' 18. | 29. November 2011', ' 08. | 11. | 16. | 29. Dezember 2011', ' 27. Januar 2012', ' 03. | 10. | 15. | 26. Februar 2012', ' 27. M\xc3\xa4rz 2012']"
            dates_per_month = dates_part.split(',')
            # dates_of_one_month = " 10. | 14. | 18. September 2011"
            for dates_of_one_month in dates_per_month:
                # raw_dates = "[' 10. ', ' 14. ', ' 18. September 2011']"
                raw_dates = dates_of_one_month.split('|')
                # raw_date_with_month_name = " 18. September 2011"
                raw_date_with_month_name = raw_dates[-1]
                # month = "September"
                month = raw_date_with_month_name.split()[1]
                # year = "2011"
                year = raw_date_with_month_name.split()[2]
                # i = "0"
                for i in range(len(raw_dates) - 1):
                    # date = "10. September 2011"
                    date = raw_dates[i].lstrip() + month + ' ' + year
                    dates.append(date)
                    
                dates.append(raw_dates[-1])
            logger.info('%s - set dates: %s', self.title, dates)
        except:
            logger.warning('Failed to set dates for play "%s". Therefore setting dates to an empty list.', self.title)
        
        return dates 
    
    def _setLocation(self):
        location = Lepistant.NOT_AVAILABLE
        
        try:
            # location_string = "Neues Schauspielhaus / Termine: 10. | 14. | 18. September 2011, 01. | 16. | 22. Oktober 2011, 18. | 29. November 2011, 08. | 11. | 16. | 29. Dezember 2011, 27. Januar 2012, 03. | 10. | 15. | 26. Februar 2012, 27. März 2012"    
            location_string = self.play_item_soup.findAll('p')[1].span.nextSibling
            # Ignore warning since we only need the location_part anyway.
            (location_part, seperator, dates_part) = location_string.partition('/')
            location = location_part.lstrip().rstrip()
            logger.info('%s - set location: "%s"', self.title, location)
        except:
            logger.warning('Failed to set location for play "%s". Therefore setting location to %s.', self.title, Lepistant.NOT_AVAILABLE)
        
        return location
    
    def _setPerformances(self):
        performances = list()
        try:
            # Since "Theater Bremen" has always the same location for each play we can use same location for each performance.
            for date in self.dates:
                performance = Performance(date, self.location)
                performances.append(performance)
                logger.info('%s - set performance: %s', self.title, performance.__dict__)
                
            # Set performance type only for the first date
            performances[0].type = self._getPerformanceTypeOfFirstPerformance()
        except TypeError as terr:
            logger.warning('Failed to set performances for play "%s" due to: %s. Therefore setting performances to an empty list',self.title, str(terr))
            
        return performances
    
    def _setSubtitle(self):
        subtitle = Lepistant.NOT_AVAILABLE
        
        try:
            subtitle_string = self.play_item_soup.p.string
            subtitle = subtitle_string.lstrip().rstrip()
            logger.info('%s - set subtitle: "%s"', self.title, subtitle)
        except:
            logger.warning('Failed to set subtitle for play "%s". Therefore setting subtitle to %s.',self.title, Lepistant.NOT_AVAILABLE)
            
        return subtitle
    
    def _setTitle(self):
        title = Lepistant.NOT_AVAILABLE
        
        try:
            title_string = self.play_item_soup.h5.a.string
            title = title_string.lstrip().rstrip()
            logger.info('%s - set title: "%s"', title, title)
        except:
            logger.error('Failed to set title.')
            
        return title
    
    def _getPerformanceTypeOfFirstPerformance(self):
        performance_type = Lepistant.NOT_AVAILABLE
        
        try:
            performance_type_string = self.play_item_soup.div.h6.string
            # performance_type_string = "<h6>Premiere</h6>"
            performance_type = performance_type_string.lstrip().rstrip()
        except:
            logger.warning('Failed to get performance type for play "%s". Therefore returning "%s".',self.title, Lepistant.NOT_AVAILABLE)
            
        return performance_type
    
    
    # 'Private assistant methods for getting the play details information.
#    def _getPhotoURLLinksFrom(self, div):
    
    def _getParagraphsForContent(self, content):
        paragraphs = list()
        
        try:
            paragraphs = self.play_detail_soup.find(text=content).findNext('div', {"class": 'toggleable-content-open'}).findAll('p')
        except:
            logger.warning('Failed to get paragraphs for play "%s". Therefore returning an empty list.', self.title)
            
        return paragraphs;
    
    def _removeBrTagsFromSoup(self, soup):
        try:
            while soup.br:
                subtree = soup.br
                subtree.extract()
        except:
            logger.warning('Failed to remove \<br\> tags from soup. Therefore returning the soup as it was. soup: %s', repr(soup[:Lepistant.LOG_MESSAGE_LENGTH]))
            
        return soup
    
    def _setSummary(self):
        self.summary = Lepistant.NOT_AVAILABLE
        
        try:
            summary_paragraphs = self._getParagraphsForContent('Inhalt')
            self.summary = Lepistant.formatParagraphsToString(summary_paragraphs)
            logger.info('%s - set summary: "%s..."', self.title, repr(self.summary[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set summary for play "%s". Therefore setting summary to %s.', self.title, Lepistant.NOT_AVAILABLE)
                
    def _setCritics(self):
        self.critics = Lepistant.NOT_AVAILABLE
        
        try:
            critics_paragraphs = self._getParagraphsForContent('Pressestimmen')
            self.critics = Lepistant.formatParagraphsToString(critics_paragraphs)
            logger.info('%s - set critics: "%s..."', self.title, repr(self.critics[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set critics for play "%s". Therefore setting critics to %s.', self.title, Lepistant.NOT_AVAILABLE)
    
    def _setFurtherInfo(self):
        self.further_info = Lepistant.NOT_AVAILABLE
        
        try:
            further_info_paragraphs = self._getParagraphsForContent('Weitere Texte')
            self.further_info = Lepistant.formatParagraphsToString(further_info_paragraphs)
            logger.info('%s - set further_info: "%s..."', self.title, repr(self.further_info[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set further_info for play "%s". Therefore setting further_info to %s.', self.title, Lepistant.NOT_AVAILABLE)
    
    def _setPhotos(self):
        photos = list()
        
        try:
            img_tags = self.play_detail_soup.find('div', {"class": "thumbnails"}).findAll('img')
            for img_tag in img_tags:
                img_url = Lepistant.getURLFromImageTag(img_tag)
                photos.append(img_url)
            logger.info('%s - set photos: %s', self.title, photos)
        except AttributeError as attrerr:
            logger.warning('Failed to set photos for play "%s" due to: %s. Therefore setting photos to an empty list.', self.title, str(attrerr))
        
        self.photos = photos
    
    def _setSponsors(self):
        sponsors = list()
        
        try:
            img_tags = self.play_detail_soup.find('div', {"class": "sponsors clearfix"})
            for img_tag in img_tags:
                img_url = Lepistant.getURLFromImageTag(img_tag)
                sponsors.append(img_url)
            logger.info('%s - set sponsors: %s', self.title, sponsors)
        except AttributeError as attrerr:
            logger.warning('Failed to set sponsor logos for play "%s" due to: %s. Therefore setting sponsors to an empty list.', self.title, str(attrerr))

        self.sponsors = sponsors
    
    def _setCast(self):
        cast = dict()
        
        try:
            artist_item_tags = self.play_detail_soup.findAll('h4', text=re.compile('Besetzung'))[0].parent.findNextSiblings(['span', 'a', 'br'])
            artist_items = [list(tag[1]) for tag in groupby(artist_item_tags, lambda tag: str(tag) == '<br />') if not tag[0]]
            
            artist_data = artist_items[0]
            
            artist = Artist(artist_data)
            # TODO: Check if this particular artist already exists. If he does only update his data
            # Getting the last added producer role of this artist.
            role = artist.producer_roles[-1]             
            if role and role in PRODUCERS_CAST:
                cast[role] = artist
                logger.info('%s - added artist  to producer\'s cast: {"%s": "%s"}', self.title, role, artist.full_name)
                print('Added the role "' + role + '" to the producer\'s cast')
        except AttributeError as attrerr:
            logger.error('Failed to set cast for play "%s" due to: %s.', self.title, str(attrerr))
    
    # 'Public' methods:
    def setPlayDetails(self, soup):
        self.play_detail_soup = soup
        self._setSummary()
        self._setCritics()
        self._setFurtherInfo()
        self._setSponsors()
        self._setCast()
        