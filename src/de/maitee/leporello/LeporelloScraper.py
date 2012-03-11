# coding: utf-8

'''
Created on Feb 19, 2012

@author: kms
'''

# Standard libraries
import logging.config
from pprint import pprint
# Third party libraries
# Local libraries
import LoggingConfig
from PlayDict import Play
from LeporelloDict import Leporello
from LeporelloAssistant import Lepistant


# Set logger from dictionary
logging.config.dictConfig(LoggingConfig.LOGGING_CONFIG)
logger = logging.getLogger('leporello')


if __name__ == '__main__':

    # Defining some constants to avoid spelling mistakes.
    URL_LEPORELLO = 'URL_LEPORELLO'
    URL_ROOT_PREFIX = 'URL_ROOT_PREFIX'
    URL_PLAY_PREFIX = 'URL_PLAY_PREFIX'
    REGEXP_PLAY_LINK_TAG = 'REGEXP_PLAY_LINK_TAG'
    CSS_CLASS_CONTENT_ITEM = 'CSS_CLASS_CONTENT_ITEM'
    CSS_CLASS_PLAY_ITEM = 'CSS_CLASS_PLAY_ITEM'
    PLAY_ITEMS = 'PLAY_ITEMS'
    
    PREMIERE = 'Premiere'
    FILE_NAME_STARTING_PAGE = 'leporello.html'
    NOT_AVAILABLE = 'n/a'
    
    # Creating the 'leporello' dictionary that servers as our root container.
    leporello = {
                 'theatre': "Theater Bremen", 
                 'season': "2011/2012", 
                 'website': "http://www.theaterbremen.de/de_DE/home", 
                 'boxOffice': "04213653333", 
                 'email': "service@theaterbremen.de", 
                 'plays': "LIST of all plays", 
                 }
    
    leporello_info = {
                     'theatre': "Theater Bremen",
                     'URL_LEPORELLO': "http://www.theaterbremen.de/de_DE/spielplan/premieren/premieren", 
                     'URL_ROOT_PREFIX': "http://www.theaterbremen.de", 
                     'URL_PLAY_PREFIX': "/de_DE/spielplan/stueck", 
                     'REGEXP_PLAY_LINK_TAG': "/de_DE/spielplan/stueck/([\d]+)", 
                     'CSS_CLASS_PLAY_ITEM': "spielplan-item", 
                     'CSS_CLASS_CONTENT_ITEM': "toggleable-content-open", 
                     'PLAY_ITEMS': "List of all play item divs containing the HTML code",    # Meta information
                      }
    
    def getPlays(leporello_info):
        plays = []
        
        # Initializing the Leporello Assistent with meta information for web scraping.
        Lepistant.setInfo(leporello_info)
        
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
        
    #    pprint(play.__dict__)
        
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
        
    #    play = createPlay(title)
    #    getLocationFromPlayItem()
    #    getURLFromPlayItem()
        
    #    print playItems[0]
    #    print dates
        
        return plays
        
    
    def pretty(dictionary, indent=0):
        pprint(dictionary.__dict__)
        for key, value in dictionary.iteritems():
            if key != ('play_detail_soup', 'soup_details', 'data_list', 'soup'):
                print '\t' * indent + str(key)
                if isinstance(value, dict):
                    pretty(value, indent + 1)
                else:
                    print '\t' * (indent + 1) + str(value)

    
    
    def printPlays(plays):
        for play in plays:
            print('')
            print('=======================================================================================================================================')
            print('')
            print('title: ' + play.title)
            print('subtitle: ' + play.subtitle)
            print('location: ' + play.location)
            print('author: ' + play.author)
            print('photos: ' + repr(play.photos))
            print('summary: ' + play.summary[:100] + '...')
            print('further_info: ' + play.further_info[:100] + '...')
            print('critits: ' + play.critics[:100] + '...')
            print('dates: ' + repr(play.dates))
            print('producer_cast: ')
            pprint(play.producer_cast)
            print('artist_default_cast: ')
            pprint(play.artist_default_cast)
            print('sponsors: ' + repr(play.sponsors))
            print('performances: ')
            pprint(play.performances)
            print('video: ' + play.video)
            print('file_name_on_disk: ' + play.file_name_on_disk)
        
        
    
    
    # Starting our leporello_info scraper
    
    # Initializing our leporello (dictionary)
    leporello = Leporello()
    leporello.plays = getPlays(leporello_info)
    
#    printPlays(plays)
    pretty(leporello)
    logger.info('Finished parsing leporello.')
