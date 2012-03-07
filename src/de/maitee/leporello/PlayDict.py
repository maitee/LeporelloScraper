# coding: utf-8

'''
Created on Feb 27, 2012

@author: kms
'''
# Standard libraries
import re
from itertools import groupby
# Local libraries
from LeporelloAssistant import Lepistant
from ArtistDict import Artist
from PerformanceDict import Performance

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

        self.link = None
        self.file_name_on_disk = None
        
        self.author = None
        self.type = None
        self.summary = str()
        self.further_info = None
        self.critics = None
        self.video = None
        self.photos = list()
        self.cast = dict()
        self.sponsors = list()
        
        self.play_detail_soup = None
        
    # 'Private' methods:
    def _setTitle(self):
        try:
            title_string = self.play_item_soup.h5.a.string
            title = title_string.lstrip().rstrip()
        except:
            print('>>>>>>>>>> Could not find any title in play_item_soup: ' + str(self.play_item_soup))
            print('>>>>>>>>>> Setting title to: ' + Lepistant.NOT_AVAILABLE)
            title = Lepistant.NOT_AVAILABLE
            
        return title
    
    def _setSubtitle(self):
        try:
            subtitle_string = self.play_item_soup.p.string
            subtitle = subtitle_string.lstrip().rstrip()
        except:
            print('>>>>>>>>>> Could not find any subtitle in play_item_soup: ' + str(self.play_item_soup))
            print('>>>>>>>>>> Setting subtitle to: ' + Lepistant.NOT_AVAILABLE)
            subtitle = Lepistant.NOT_AVAILABLE
            
        return subtitle
    
    def _setLocation(self):
        try:
            # location_string = "Neues Schauspielhaus / Termine: 10. | 14. | 18. September 2011, 01. | 16. | 22. Oktober 2011, 18. | 29. November 2011, 08. | 11. | 16. | 29. Dezember 2011, 27. Januar 2012, 03. | 10. | 15. | 26. Februar 2012, 27. März 2012"    
            location_string = self.play_item_soup.findAll('p')[1].span.nextSibling
            # Ignore warning since we only need the location_part anyway.
            (location_part, seperator, dates_part) = location_string.partition('/')
            location = location_part.lstrip().rstrip()
        except:
            print('>>>>>>>>>> Could not find any location in play_item_soup: ' + str(self.play_item_soup))
            print('>>>>>>>>>> Setting location to: ' + Lepistant.NOT_AVAILABLE)
            location = Lepistant.NOT_AVAILABLE
        
        return location
    
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
        except:
            print('>>>>>>>>>> Could not find any dates in play_item_soup: ' + str(self.play_item_soup))
            print('>>>>>>>>>> Setting dates to an empty list')
        
        return dates 
    
    def _setPerformances(self):
        performances = list()
    
        # Since "Theater Bremen" has always the same location for each play we can use same location for each performance.
        for date in self.dates:
            performance = Performance(date, self.location)
            performances.append(performance)
            
        # Set performance type only for the first date
        performances[0].type = self._getPerformanceTypeOfFirstPerformance()
        
        return performances
    
    def _getPerformanceTypeOfFirstPerformance(self):
        try:
            performance_type_string = self.play_item_soup.div.h6.string
            # performance_type_string = "<h6>Premiere</h6>"
            performance_type = performance_type_string.lstrip().rstrip()
        except:
            print('>>>>>>>>>> Could not find any performance type in play_item_soup: ' + str(self.play_item_soup))
            performance_type = Lepistant.NOT_AVAILABLE
            
        return performance_type
    
    
    # 'Private assistant methods for getting the play details information.
#    def _getPhotoURLLinksFrom(self, div):
    
    def _getParagraphsForContent(self, content):
        paragraphs = self.play_detail_soup.find(text=content).findNext('div', {"class": 'toggleable-content-open'}).findAll('p')
        
        return paragraphs;
    
    def _removeBrTagsFromSoup(self, soup):
        while soup.br:
            subtree = soup.br
            subtree.extract()
        
        return soup
    
    def _setSummary(self):
        summary_paragraphs = self._getParagraphsForContent('Inhalt')
        self.summary = Lepistant.formatParagraphsToString(summary_paragraphs)
#        print self.summary
                
    def _setCritics(self):
        critics_paragraphs = self._getParagraphsForContent('Pressestimmen')
        self.critics = Lepistant.formatParagraphsToString(critics_paragraphs)
#        print self.critics
    
    def _setFurtherInfo(self):
        further_info_paragraphs = self._getParagraphsForContent('Weitere Texte')
        self.further_info = Lepistant.formatParagraphsToString(further_info_paragraphs)
#        print self.further_info
    
    def _setPhotos(self):
        try:
            img_tags = self.play_detail_soup.find('div', {"class": "thumbnails"}).findAll('img')
            for img_tag in img_tags:
                img_url = Lepistant.getURLFromImageTag(img_tag)
                self.photos.append(img_url)
        except AttributeError as attrerr:
            print('>>>>>>>>>> Could not set photos due to: See next line.')
            print('>>>>>>>>>> Could not find img tags due to: ' + str(attrerr))
    
    def _setSponsors(self):
        try:
            img_tags = self.play_detail_soup.find('div', {"class": "sponsors clearfix"})
            for img_tag in img_tags:
                img_url = Lepistant.getURLFromImageTag(img_tag)
                self.sponsors.append(img_url)
        except AttributeError as attrerr:
            print('>>>>>>>>>> Could not set sponsors due to: See next line.')
            print('>>>>>>>>>> Could not find img tags due to: ' + str(attrerr))
    
    
    def _setCast(self):
        try:
            print('>>>>>>>>>> in PlayDict._setCast() <<<<<<<<<<')
            artist_item_tags = self.play_detail_soup.findAll('h4', text=re.compile('Besetzung'))[0].parent.findNextSiblings(['span', 'a', 'br'])
            artist_items = [list(tag[1]) for tag in groupby(artist_item_tags, lambda tag: str(tag) == '<br />') if not tag[0]]
            
            artist_data = artist_items[0]
            
            artist = Artist(artist_data)
            # TODO: Check if this particular artist already exists. If he does only update his data
            # Getting the last added producer role of this artist.
            role = artist.producer_roles[-1]             
            if role and role in PRODUCERS_CAST:
                self.cast[role] = artist
                print('Added the role "' + role + '" to the producer\'s cast')
            
        except AttributeError as attrerr:
            print('>>>>>>>>>> Could not set artist data due to parsing error in the soup: ' + str(attrerr))
    
    # 'Public' methods:
    def setPlayDetails(self, soup):
        self.play_detail_soup = soup
        self._setSummary()
#        print self.summary
        self._setCritics()
#        print self.critics
        self._setFurtherInfo()
#        print self.further_info
        self._setPhotos()
#        print self.photos
        self._setSponsors()
#        print self.sponsors
        self._setCast()
#        print self.cast
        