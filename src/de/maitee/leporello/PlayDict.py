# coding: utf-8

'''
Created on Feb 27, 2012

@author: kms
'''
# Standard libraries
import re
import locale
import logging
import datetime
from itertools import groupby
# Local libraries
from LeporelloAssistant import Lepistant
from ArtistDict import Artist
from PerformanceDict import Performance


logger = logging.getLogger('leporello')


# Member names of producer's producer_cast.
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

class Play(dict):
    '''
    classdocs
    '''

    def __init__(self, play_item_soup):
        '''
        Constructor
        '''
        dict.__init__(self, {})
        
        self.play_item_soup = play_item_soup
        self.title = self._setTitle()
        self.subtitle = self._setSubtitle()
        self.default_location = self._setLocation()
        self.dates = self._setDates()

        self.link = str()
        self.file_path_on_disk = str()
        self.file_name_on_disk = str()
        
        self.author = str()
        self.type = str()
        self.summary = str()
        self.further_info = str()
        self.critics = str()
        self.video = str()
        self.photos = list()
        self.producer_cast = None                  # dict
        self.artist_default_cast = None             # dict
        self.sponsors = list()
        self.performances = dict()
        
        self.play_detail_soup = None
        
    # 'Private' methods:
    def _setKey(self, key, value):
        self[key] = value
        
        return value
        
    
    def _setDates(self):
        dates = list()
        
        try:
            # Set locale time from en_US to de_DE for formatting calendar dates.
            locale.setlocale(locale.LC_TIME, 'de_DE.utf-8')
            
            dates_string = self.play_item_soup.findAll('p')[1].span.nextSibling
            # dates_string = "Neues Schauspielhaus / Termine: 10. | 14. | 18. September 2011, 01. | 16. | 22. Oktober 2011, 18. | 29. November 2011, 08. | 11. | 16. | 29. Dezember 2011, 27. Januar 2012, 03. | 10. | 15. | 26. Februar 2012, 27. März 2012"
            (location_part, seperator, dates_part) = dates_string.partition(':') 
            dates_per_month = dates_part.split(',')
            # dates_per_month = "[' 10. | 14. | 18. September 2011', ' 01. | 16. | 22. Oktober 2011', ' 18. | 29. November 2011', ' 08. | 11. | 16. | 29. Dezember 2011', ' 27. Januar 2012', ' 03. | 10. | 15. | 26. Februar 2012', ' 27. M\xc3\xa4rz 2012']"
           
            for dates_of_one_month in dates_per_month:
            # dates_of_one_month = " 10. | 14. | 18. September 2011"
                raw_dates = dates_of_one_month.split('|')
                # raw_dates = "[' 10. ', ' 14. ', ' 18. September 2011']"
                raw_date_with_month_name = raw_dates[-1]
                # raw_date_with_month_name = " 18. September 2011"
                month = raw_date_with_month_name.split()[1]
                # month = "September"
                year = raw_date_with_month_name.split()[2]
                # year = "2011"
                
                for i in range(len(raw_dates) - 1):
                # i = "0"
                    # date = "10. September 2011"
                    date_string_raw = raw_dates[i].lstrip() + month + ' ' + year
                    date_time = datetime.datetime.strptime(date_string_raw, '%d. %B %Y')
                    
                    # For json serialization we have to save the date as a string.
                    date_string = Lepistant.formatDatetimeToString(date_time)
                    dates.append(date_string)
                
                # Formatting the last date in the list: "18. September 2011"
                last_date_unformatted = raw_dates[-1].lstrip().rstrip()
                last_date_time = datetime.datetime.strptime(last_date_unformatted, '%d. %B %Y')
                last_date_string = Lepistant.formatDatetimeToString(last_date_time)
                
                dates.append(last_date_string)
                
            logger.info('%s - set dates: %s', self.title, dates)
        except ValueError as verr:
            logger.error('Failed to format date "%s" for play "%s" due to: %s', date_string_raw, self.title, str(verr))
        except:
            logger.error('')
            logger.error('Failed to set dates for play "%s". Therefore setting dates to an empty list.', self.title)
            logger.error('')
        
        # Set locale time back from de_DE to en_US.
        locale.setlocale(locale.LC_TIME, 'en_US.utf-8')
        
        logger.info('')
        return self._setKey('dates', dates)
    
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
        
        logger.info('')
        
        return self._setKey('default_location', location)
    
    def _getFurtherPerformances(self):
        # Set locale time from en_US to de_DE for formatting calendar dates.
        locale.setlocale(locale.LC_TIME, 'de_DE.utf-8')
        
        perfomance_tuples = list()
        
        try:
            performance_tags = self.play_detail_soup.find('div', {"class": "further-performances"}).findAll('div')
            
            for perfomance_tag in performance_tags:
                date_link_tag = perfomance_tag.findAll('a', text=True)[0].parent
                date_string = date_link_tag.string
                date_time = datetime.datetime.strptime(date_string, '%a, %d.%m.%Y / %H.%M Uhr')
                date = Lepistant.formatDatetimeToString(date_time)
                url = Lepistant.getURLFromLinkTag(date_link_tag)
                performance_tuple = (date, url)
                perfomance_tuples.append(performance_tuple)
        except:
            logger.warning('Failed to get further performances for play "%s". Therefore returning an empty list.', self.title)
        
        # Set locale time back from de_DE to en_US.
        locale.setlocale(locale.LC_TIME, 'en_US.utf-8')
        
        return perfomance_tuples
    
    def _setDetailsForPerformances(self):
        performance_tuples = self._getFurtherPerformances()
        
        if performance_tuples:
            for a_tuple in performance_tuples:
                date = a_tuple[0]
                
                # Only use year, month and day to look up dates for performances.
                date_lookup = date.split('-')[0] + '-00.00'
                
                url = a_tuple[1]
                file_path = Lepistant.createFilePath(self.file_path_on_disk, date, 'performance')
                soup = Lepistant.getSoup(url, file_path)
                
                if date_lookup in self.performances:
                    # Updating the date with a more precise date including Weekday and Time.
                    performance = self.performances[date_lookup]
                    # TODO: Updating of the date should be done in single function.
                    performance.date = date
                    performance['date'] = date
                    
                    performance.setDetails(soup, self.title)
        
    def _setPerformances(self):
        performances = dict()
        
        try:
            # Since "Theater Bremen" has always the same location for each play we can use the same location for each performance.
            if self.dates:
                for date in self.dates:
                    performance = Performance(date, self.default_location, self.artist_default_cast)
                    performances[date] = performance
                    logger.info('%s - added performance: %s', self.title, performance.__dict__)
                    
                # Set performance type only for the first date
                first_performance = performances[self.dates[0]]
                # TODO: Check if dot setting also changes key/value.
                first_performance.type = self._getPerformanceTypeOfFirstPerformance()
                logger.info('%s - set type to "%s" of performance: %s', self.title, first_performance.type, first_performance.__dict__)
            else:
                logger.warning('Failed to set performances for play "%s" because no dates were found. Therefore setting performances to an empty list', self.title)
        except TypeError as terr:
            logger.warning('Failed to set performances for play "%s" due to: %s. Therefore setting performances to an empty list', self.title, str(terr))
            
        self.performances = self._setKey('performances', performances)
        
        self._setDetailsForPerformances()
    
    def _setSubtitle(self):
        subtitle = Lepistant.NOT_AVAILABLE
        
        try:
            subtitle_string = self.play_item_soup.p.string
            subtitle = subtitle_string.lstrip().rstrip()
            logger.info('%s - set subtitle: "%s"', self.title, subtitle)
        except:
            logger.warning('Failed to set subtitle for play "%s". Therefore setting subtitle to %s.',self.title, Lepistant.NOT_AVAILABLE)
        
        logger.info('')
            
        return self._setKey('subtitle', subtitle)
    
    def _setTitle(self):
        title = Lepistant.NOT_AVAILABLE
        
        try:
            title_string = self.play_item_soup.h5.a.string
            title = title_string.lstrip().rstrip()
            logger.info('%s - set title: "%s"', title, title)
        except:
            logger.error('Failed to set title.')
        
        logger.info('')
        
        return self._setKey('title', title)
    
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
        summary = Lepistant.NOT_AVAILABLE
        
        try:
            summary_paragraphs = self._getParagraphsForContent('Inhalt')
            summary = Lepistant.formatParagraphsToString(summary_paragraphs)
            logger.info('%s - set summary: "%s..."', self.title, repr(summary[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set summary for play "%s". Therefore setting summary to %s.', self.title, Lepistant.NOT_AVAILABLE)
            
        self.summary = self._setKey('summary', summary)
                
    def _setCritics(self):
        critics = Lepistant.NOT_AVAILABLE
        
        try:
            critics_paragraphs = self._getParagraphsForContent('Pressestimmen')
            critics = Lepistant.formatParagraphsToString(critics_paragraphs)
            logger.info('%s - set critics: "%s..."', self.title, repr(critics[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set critics for play "%s". Therefore setting critics to %s.', self.title, Lepistant.NOT_AVAILABLE)
            
        self.critics = self._setKey('critics', critics)
    
    def _setFurtherInfo(self):
        further_info = Lepistant.NOT_AVAILABLE
        
        try:
            further_info_paragraphs = self._getParagraphsForContent('Weitere Texte')
            further_info = Lepistant.formatParagraphsToString(further_info_paragraphs)
            logger.info('%s - set further_info: "%s..."', self.title, repr(further_info[:Lepistant.LOG_MESSAGE_LENGTH]))
        except:
            logger.warning('Failed to set further_info for play "%s". Therefore setting further_info to %s.', self.title, Lepistant.NOT_AVAILABLE)
    
        self.further_info = self._setKey('further_info', further_info)
    
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
        
        self.photos = self._setKey('photos', photos)
    
    def _setSponsors(self):
        sponsors = list()
        
        try:
            img_tags = self.play_detail_soup.find('div', {"class": "sponsors clearfix"})
            if img_tags:
                for img_tag in img_tags:
                    img_url = Lepistant.getURLFromImageTag(img_tag)
                    sponsors.append(img_url)
                logger.info('%s - set sponsors: %s', self.title, sponsors)
            else:
                logger.info('%s - Play does not have any sponsors. Therefore setting sponsors to an empty list.', self.title)
        except AttributeError as attrerr:
            logger.warning('Failed to set sponsor logos for play "%s" due to: %s. Therefore setting sponsors to an empty list.', self.title, str(attrerr))

        self.sponsors = self._setKey('sponsors', sponsors)
    
#    @classmethod
#    def getRoleFromArtistItem(cls, artist_item):
#        role = Lepistant.NOT_AVAILABLE
#        
#        for element in artist_item:
#            if 'class="eventDetailPersonRole"' in str(element):
#                try:
#                    role = element.string.split(':')[0]
#                except:
#                    logger.info('Setting role to "%s" since no role could be find in data_list: %s', role, artist_item)
#        
#        return role
    
    def _setCast(self):
        producer_cast = dict()
        artist_default_cast = dict()
        
        try:
            artist_item_tags = self.play_detail_soup.findAll('h4', text=re.compile('Besetzung'))[0].parent.findNextSiblings(['span', 'a', 'br'])
            
            if artist_item_tags:
                artist_items = [list(tag[1]) for tag in groupby(artist_item_tags, lambda tag: str(tag) == '<br />') if not tag[0]]
                
                for artist_item in artist_items:
                    artist = Artist(artist_item)
                    role = Performance.getRoleFromArtistItem(artist_item)
                    
                    if role:
                        if role in PRODUCERS_CAST:
                            producer_cast[role] = artist.full_name
                            logger.info('%s - added artist to producer_cast: {"%s": "%s"}', self.title, role, artist.full_name)
                        else:
                            if role == Lepistant.NOT_AVAILABLE:
                                role = artist.full_name
                            
                            artist_default_cast[role] = artist.full_name
                            logger.info('%s - added artist to artist_default_cast: {"%s": "%s"}', self.title, role, artist.full_name)
                
                self.producer_cast = self._setKey('producer_cast', producer_cast)
                self.artist_default_cast = self._setKey('artist_default_cast', artist_default_cast)
            else:
                logger.info('%s - Play does not have a producer_cast. Therefore setting producer_cast and artist_default_cast to an empty dictionary.', self.title)
        except IndexError as ierr:
            logger.warning('Failed to set producer_cast for play "%s" due to: %s.', self.title, str(ierr))
        except AttributeError as attrerr:
            logger.warning('Failed to set producer_cast for play "%s" due to: %s.', self.title, str(attrerr))
            
    
    # 'Public' methods:
    def setPlayDetails(self, soup):
        self.play_detail_soup = soup
        logger.info('')
        self._setSummary()
        logger.info('')
        self._setCritics()
        logger.info('')
        self._setFurtherInfo()
        logger.info('')
        self._setSponsors()
        logger.info('')
        self._setCast()
        logger.info('')
        self._setPerformances()
        logger.info('')
        self._setDetailsForPerformances()
        