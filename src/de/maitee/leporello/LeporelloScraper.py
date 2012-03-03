# coding: utf-8

'''
Created on Feb 19, 2012

@author: kms
'''

# Standard libraries
from pprint import pprint
# Third party libraries
# Local libraries
from PlayDict import Play
from LeporelloAssistent import Lepistent

if __name__ == '__main__':
    pass

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
    # Creating the 'plays' list that holds all 'play's of the leporello_info
    plays = dict()
    
    # Initializing the Leporello Assistent with meta information for web scraping.
    Lepistent.setInfo(leporello_info)
    
    leporelloFileNameOnDisk = Lepistent.createFilePath(
                                            Lepistent.REL_PATH_DOWNLOADS_FOLDER, 
                                            Lepistent.FILE_NAME_LEPORELLO, 
                                            '.leporello')
    soup = Lepistent.getSoup(leporello_info[URL_LEPORELLO], 
                             leporelloFileNameOnDisk)
    playItems = Lepistent.getTagsByClass(soup, 'div', 
                                         leporello_info[CSS_CLASS_PLAY_ITEM])
    leporello_info[PLAY_ITEMS] = playItems
    
    # Get only one play item for testing purposes
    playItem = playItems[12]
    play = Play(playItem)
    play.link = Lepistent.getURLFromTagContent(playItem)
    play.file_name_on_disk = Lepistent.createFilePath(
                                            Lepistent.REL_PATH_DOWNLOADS_FOLDER, 
                                            play.title, 
                                            '.html')
    soup = Lepistent.getSoup(play.link, play.file_name_on_disk)
    play.setPlayDetails(soup)
    
#    pprint(play.__dict__)
    
#    for playItem in playItems:
#        play = Play(playItem)
#        play.link = Lepistent.getURLFromTagContent(playItem)
#        play.file_name_on_disk = Lepistent.createFilePath(
#                                            Lepistent.REL_PATH_DOWNLOADS_FOLDER, 
#                                            play.title, 
#                                            '.html')
#        soup = Lepistent.getSoup(play.link, play.file_name_on_disk)
#        plays[play.title] = play
    
#    play = createPlay(title)
#    getLocationFromPlayItem()
#    getURLFromPlayItem()
    
#    print playItems[0]
#    print dates
    
    return plays


# Starting ou leporello_info scraper
plays = getPlays(leporello_info)
#pprint(plays)
print "finished"