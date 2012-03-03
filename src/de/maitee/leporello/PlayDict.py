# coding: utf-8

'''
Created on Feb 27, 2012

@author: kms
'''
# Standard libraries
# Local libraries
from PerformanceDict import Performance
from LeporelloAssistent import Lepistent

# Default value for unavailable keys.
NOT_AVAILABLE = 'n/a'

class Play(dict, Lepistent):
    '''
    classdocs
    '''

    def __init__(self, play_item):
        '''
        Constructor
        '''
        dict.__init__({})
        self.play_item = play_item
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
        
        self.play_details = None
        
    # 'Private' methods:
    def _setTitle(self):
        try:
            title_string = self.play_item.h5.a.string
            title = title_string.lstrip().rstrip()
        except:
            print('Could not find any title in play_item: ' + str(self.play_item))
            title = NOT_AVAILABLE
            
        return title
    
    def _setSubtitle(self):
        try:
            subtitle_string = self.play_item.p.string
            subtitle = subtitle_string.lstrip().rstrip()
        except:
            print('Could not find any subtitle in play_item: ' + str(self.play_item))
            subtitle = NOT_AVAILABLE
            
        return subtitle
    
    def _setLocation(self):
        try:
            # location_string = "Neues Schauspielhaus / Termine: 10. | 14. | 18. September 2011, 01. | 16. | 22. Oktober 2011, 18. | 29. November 2011, 08. | 11. | 16. | 29. Dezember 2011, 27. Januar 2012, 03. | 10. | 15. | 26. Februar 2012, 27. März 2012"    
            location_string = self.play_item.findAll('p')[1].span.nextSibling
            (location_part, seperator, dates_part) = location_string.partition('/')
            location = location_part.lstrip().rstrip()
        except:
            print('Could not find any location in play_item: ' + str(self.play_item))
            location = NOT_AVAILABLE
        
        return location
    
    def _setDates(self):
        dates = list()
        try:
            dates_string = self.play_item.findAll('p')[1].span.nextSibling
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
            print('Could not find any dates in play_item: ' + str(self.play_item))
        
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
            performance_type_string = self.play_item.div.h6.string
            # performance_type_string = "<h6>Premiere</h6>"
            performance_type = performance_type_string.lstrip().rstrip()
        except:
            print('Could not find any performance type in play_item: ' + str(self.play_item))
            performance_type = NOT_AVAILABLE
            
        return performance_type
    
    
    # 'Private assistant methods for getting the play details information.
#    def _getPhotoURLLinksFrom(self, div):
    
    def _getParagraphsForContent(self, content):
        paragraphs = self.play_details.find(text=content).findNext('div', {"class": 'toggleable-content-open'}).findAll('p')
        
        return paragraphs;
    
    def _removeBrTagsFromSoup(self, soup):
        while soup.br:
            subtree = soup.br
            subtree.extract()
        
        return soup
    
    def _replaceBrTagsInSoup(self, soup, tag_replacement):
        while soup.br:
            soup.br.replaceWith('\n')
            
        return soup
    
    def _concatenatingStringsFromParagraphs(self, paragraphs):
        concatenated_string = ''
        
        if paragraphs:
            for paragraph in paragraphs:
                ''' The following method is not working. Don't know why. ''' 
        #        Lepistent.removeSubtreesFromSoup(paragraph, lambda: paragraph.br)
        #        print summary_paragraph
                
                ''' Removing the br tags here since the above method is not working. '''
                paragraph = self._replaceBrTagsInSoup(paragraph, '\n')
                
                # Concatenating the content's lines by assigning them to concatenated_string
                for line in paragraph.contents:
                    concatenated_string += line.string
                
        return concatenated_string
                
    def _setSummary(self):
        summary_paragraphs = self._getParagraphsForContent('Inhalt') 
        self.summary = self._concatenatingStringsFromParagraphs(summary_paragraphs)
                
    def _setCritics(self):
        critics_paragraphs = self._getParagraphsForContent('Pressestimmen')
        self.critics = self._concatenatingStringsFromParagraphs(critics_paragraphs)
    
    def _setFurtherInfo(self):
        further_info_paragraphs = self._getParagraphsForContent('Weitere Texte')
        self.further_info = self._concatenatingStringsFromParagraphs(further_info_paragraphs)
    
    # 'Public' methods:
    def setPlayDetails(self, soup):
        self.play_details = soup
        self._setSummary()
#        print self.summary
        self._setCritics()
#        print self.critics
        self._setFurtherInfo()
#        print self.further_info
#        self.photos = self._getPhotos()
#        self.sponsors = self._getSponsors()
#        self.cast = self._getCast()
        