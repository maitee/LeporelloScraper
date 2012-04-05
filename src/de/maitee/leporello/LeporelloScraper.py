# coding: utf-8

'''
Created on Feb 19, 2012

@author: kms
'''

# Standard libraries
import json
import logging.config
from pprint import pprint
# Third party libraries
# Local libraries
import LoggingConfig
from LeporelloAssistant import Lepistant
from LeporelloAssistant import leporello
from PlayDict import Play

# Set logger from dictionary
logging.config.dictConfig(LoggingConfig.LOGGING_CONFIG)
logger = logging.getLogger('leporello')


if __name__ == '__main__':

    # Defining some constants to avoid spelling mistakes.
    URL_LEPORELLO = 'URL_LEPORELLO'
    URL_ROOT_PREFIX = 'URL_ROOT_PREFIX'
    URL_PLAY_PREFIX = 'URL_PLAY_PREFIX'
    URL_STRAIGHT_THEATER = 'URL_STRAIGHT_THEATER'
    URL_MUSICAL_THEATER = 'URL_MUSICAL_THEATER'
    URL_DANCE_THEATER = 'URL_DANCE_THEATER'
    URL_MOKS = 'URL_MOKS'
    URL_JUNGE_AKTEURE = 'URL_JUNGE_AKTEURE'
    REGEXP_PLAY_LINK_TAG = 'REGEXP_PLAY_LINK_TAG'
    CSS_CLASS_CONTENT_ITEM = 'CSS_CLASS_CONTENT_ITEM'
    CSS_CLASS_PLAY_ITEM = 'CSS_CLASS_PLAY_ITEM'
    PLAY_ITEMS = 'PLAY_ITEMS'
    
    PREMIERE = 'Premiere'
    FILE_NAME_STARTING_PAGE = 'leporello.html'
    NOT_AVAILABLE = 'n/a'
    
    # Creating the 'leporello' dictionary that servers as our root container.
#    leporello = {
#                 'theatre': "Theater Bremen", 
#                 'season': "2011/2012", 
#                 'website': "http://www.theaterbremen.de/de_DE/home", 
#                 'boxOffice': "04213653333", 
#                 'email': "service@theaterbremen.de", 
#                 'plays': "LIST of all plays", 
#                 }
    
    
    
    leporello_info = {
                     'theatre': "Theater Bremen",
                     'URL_LEPORELLO': "http://www.theaterbremen.de/de_DE/spielplan/premieren/premieren", 
                     'URL_ROOT_PREFIX': "http://www.theaterbremen.de", 
                     'URL_PLAY_PREFIX': "/de_DE/spielplan/stueck", 
                     'URL_STRAIGHT_THEATER': "http://www.theaterbremen.de/de_DE/spielplan/premieren/schauspiel", 
                     'URL_MUSICAL_THEATER': "http://www.theaterbremen.de/de_DE/spielplan/premieren/oper", 
                     'URL_DANCE_THEATER': "http://www.theaterbremen.de/de_DE/spielplan/premieren/tanztheater", 
                     'URL_MOKS': "http://www.theaterbremen.de/de_DE/spielplan/premieren/moks", 
                     'URL_JUNGE_AKTEURE': "http://www.theaterbremen.de/de_DE/spielplan/premieren/jungeakteure", 
                     'REGEXP_PLAY_LINK_TAG': "/de_DE/spielplan/stueck/([\d]+)", 
                     'CSS_CLASS_PLAY_ITEM': "spielplan-item", 
                     'CSS_CLASS_CONTENT_ITEM': "toggleable-content-open", 
                     'PLAY_ITEMS': "List of all play item divs containing the HTML code",    # Meta information
                      }
    
    
    def getTitleFromPlayItem(play_item):
        title = Lepistant.NOT_AVAILABLE
        
        try:
            title_string = play_item.h5.a.string
            title = title_string.lstrip().rstrip()
            logger.info('Succeeded - Getting title "%s" from play_item.', title)
        except:
            logger.error('Failed to get title.')
        
        logger.info('')
        
        return title
    
    def setDefaultTimeForPerformancesInPlay(play):
        default_time = play.default_time
        
        for date_key in play.performances:
            performance = play.performances[date_key]
            performance_date = performance['date']
            performance_time = performance_date.split('T')[1]
            
            if (performance_time == '00:00') and (default_time != '00:00'):
                new_performance_date = performance_date.split('T')[0] + 'T' + default_time
                performance['date'] = new_performance_date
    
    def getSpecificTheaterPlays(leporello_info, file_name, play_type, url):
        theater_plays = []
        
        leporello_file_name_on_disk = Lepistant.createFilePath(
                                               Lepistant.REL_PATH_DOWNLOADS_FOLDER, 
                                               file_name, 
                                               'html')
        
        soup = Lepistant.getSoup(url, leporello_file_name_on_disk)
        
        theater_play_items = Lepistant.getTagsByClass(soup, 'div', leporello_info[CSS_CLASS_PLAY_ITEM])
        
#        for play_item in theater_play_items:
#            title = getTitleFromPlayItem(play_item)
#            theater_plays.append(title)
            
        for play_item in theater_play_items:
            logger.info('>>>>>>>>>>>>>>>>>>>>>>>> Fetching new play <<<<<<<<<<<<<<<<<<<<<<<<<')
            play = Play(play_item)
            play.setType(play_type)
            play.link = Lepistant.getURLFromTagContent(play_item)
            formatted_title = Lepistant.removeNonAlphanumericCharacters(play.title)
            play.file_path_on_disk = Lepistant.REL_PATH_PLAYS_FOLDER + formatted_title + '/'
            play.file_name_on_disk = Lepistant.createFilePath(
                                                play.file_path_on_disk, 
                                                play.title, 
                                                'html')
            soup = Lepistant.getSoup(play.link, play.file_name_on_disk)
            play.setPlayDetails(soup)
            
            setDefaultTimeForPerformancesInPlay(play)
            
            logger.info('')
            
            theater_plays.append(play)
            
        return theater_plays
    
    def getPlays(leporello_info):
        plays = []
        
        # Initializing the Leporello Assistent with meta information for web scraping.
#        Lepistant.setInfo(leporello_info)
        
        leporelloFileNameOnDisk = Lepistant.createFilePath(
                                                Lepistant.REL_PATH_DOWNLOADS_FOLDER, 
                                                Lepistant.FILE_NAME_LEPORELLO, 
                                                'leporello')
        
        soup = Lepistant.getSoup(leporello_info[URL_LEPORELLO], 
                                 leporelloFileNameOnDisk)
        
        playItems = Lepistant.getTagsByClass(soup, 'div', 
                                             leporello_info[CSS_CLASS_PLAY_ITEM])
        leporello_info[PLAY_ITEMS] = playItems
        
        # Get only one play item for testing purposes
#        playItem = playItems[20]    # WirAlleAnders
        playItem = playItems[12]    # AltArmArbeitslos
        play = Play(playItem)
        play.link = Lepistant.getURLFromTagContent(playItem)
        formatted_title = Lepistant.removeNonAlphanumericCharacters(play.title)
        play.file_path_on_disk = Lepistant.REL_PATH_PLAYS_FOLDER + formatted_title + '/'
        play.file_name_on_disk = Lepistant.createFilePath(
                                                play.file_path_on_disk, 
                                                play.title, 
                                                'html')
        soup = Lepistant.getSoup(play.link, play.file_name_on_disk)
        play.setPlayDetails(soup)
        plays.append(play)
        
        
#        for playItem in playItems:
#            logger.info('>>>>>>>>>>>>>>>>>>>>>>>> Fetching new play <<<<<<<<<<<<<<<<<<<<<<<<<')
#            play = Play(playItem)
#            play.link = Lepistant.getURLFromTagContent(playItem)
#            formatted_title = Lepistant.removeNonAlphanumericCharacters(play.title)
#            play.file_path_on_disk = Lepistant.REL_PATH_PLAYS_FOLDER + formatted_title + '/'
#            play.file_name_on_disk = Lepistant.createFilePath(
#                                                play.file_path_on_disk, 
#                                                play.title, 
#                                                'html')
#            soup = Lepistant.getSoup(play.link, play.file_name_on_disk)
#            play.setPlayDetails(soup)
#            
#            logger.info('')
#            
#            plays.append(play)
        
        return plays
        
    
    def createJSONFile(file_name, leporello, prettify):
        file_path = Lepistant.createFilePath(Lepistant.REL_PATH_DOWNLOADS_FOLDER, file_name, 'json')
        json_file = open(file_path, 'w+')
        json.dump(leporello, json_file, sort_keys=True, ensure_ascii=False)
        
        if (prettify):
            file_path_formatted = Lepistant.createFilePath(Lepistant.REL_PATH_DOWNLOADS_FOLDER, file_name + '_formatted', 'json')
            json_file_formatted = open(file_path_formatted, 'w+')
            json.dump(leporello, json_file_formatted, sort_keys=True, ensure_ascii=False, indent=4)
    
    
    
    
    # Starting our leporello scraper
    
    # Initializing the Leporello Assistent with meta information for web scraping.
    Lepistant.setInfo(leporello_info)
    
#    leporello['plays'] = getPlays(leporello_info)
    
    plays = list()
    
    straight_theater_plays = getSpecificTheaterPlays(leporello_info, 'SchauspielBremen', 'straight', leporello_info[URL_STRAIGHT_THEATER])
#    leporello['straight_theater'] = straight_theater_plays
#    plays.append(straight_theater_plays)
    plays.extend(straight_theater_plays)
    
    musical_theater_plays = getSpecificTheaterPlays(leporello_info, 'OperBremen', 'musical', leporello_info[URL_MUSICAL_THEATER])
#    leporello['musical_theater'] = musical_theater_plays
    plays.extend(musical_theater_plays)
    
    dance_theater_plays = getSpecificTheaterPlays(leporello_info, 'TanztheaterBremen', 'dance', leporello_info[URL_DANCE_THEATER])
#    leporello['dance_theater'] = dance_theater_plays
    plays.extend(dance_theater_plays)
    
    moks_plays = getSpecificTheaterPlays(leporello_info, 'MoksBremen', 'moks', leporello_info[URL_MOKS])
#    leporello['moks'] = moks_plays
    plays.extend(moks_plays)
    
    junge_akteure_plays = getSpecificTheaterPlays(leporello_info, 'JungeAkteure', 'young_actors', leporello_info[URL_JUNGE_AKTEURE])
#    leporello['junge_akteure'] = junge_akteure_plays
    plays.extend(junge_akteure_plays)
    
    leporello['plays'] = plays
    
    
    file_name = 'leporello_test'
    createJSONFile(file_name, leporello, True)
    
    file_name = 'leporello'
    createJSONFile(file_name, leporello, True)
    
    logger.info('Finished parsing leporello.')
    
    
