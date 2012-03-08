# coding: utf-8

'''
Created on Feb 28, 2012

@author: kms
'''

# Standard libraries
import re
import os
import pickle
import urllib2
import HTMLParser
import logging
from pickle import PickleError
# Third party libraries
from BeautifulSoup import BeautifulSoup
# Local libraries


logger = logging.getLogger('leporello')


class Lepistant(object):
    '''
    <p>
        This class provides meta and non-meta information ('leporello' Dict) about the 
        leporello website which are needed to scrape its contents.
        <b />It also provides assistant methods (static) and constants to all its 
        subclasses for general parsing tasks.
    </p>
    '''
    
    # Class attributes
    '''
    @cvar leporello: A dict that contains meta and non-meta information for parsing 
    the leporello website
    '''
    info = dict()
    
    # Default value for unavailable keys.
    NOT_AVAILABLE = 'n/a'
    
    CSS_CLASS_CONTENT_ITEM = str()   # Set by setInfo()
    
    FILE_NAME_LEPORELLO = str()     # Set by setInfo()

    LOG_MESSAGE_LENGTH = 100

    KEY_CSS_CLASS_CONTENT_ITEM = 'CSS_CLASS_CONTENT_ITEM'  
    KEY_THEATRE = 'theatre'
    KEY_URL_PREFIX = 'URL_ROOT_PREFIX'
    
    REL_PATH_DOWNLOADS_FOLDER = '../../../../downloads/'
    REL_PATH_PLAYS_FOLDER = '../../../../downloads/plays/'
    REL_PATH_ARTISTS_FOLDER = '../../../../downloads/artists/'
    
    STRING_NOT_AVAILABLE = 'n/a'
    
    URL_PREFIX = str()              # Set by setInfo()
    
    def __init__(self, leporello_info):
        '''
        Constructor
        '''
        
    
    # Class methods:
    @classmethod
    def createFilePath(cls, path, name, suffix):
        '''
        Creates a file path including the file name for pickling any kind of text files (webpages) 
        by removing all non-alphanumeric characters from the name.
        @param cls: This class to reference class variables.
        @param path: The path to the directory in which the file will be pickled.
        @param name: The name that will be formatted so it it can be used as the file name.
        @param suffix: The suffix of the file name, e.g. '.html', '.txt', ... .
        @return: (string) file_path - A formatted file path that can be used for pickling a file.
        '''
        # TODO: Implement a condition instead of exception to handle correct method according 
        # to the python version. The UNICODE flag is only supported for python >= 2.7
        # Removing all non-alphanumeric characters and appending the suffix.
        try:
            file_path = path + re.sub(r"\W+", "", name, 0, re.UNICODE) + '.' + suffix
        except TypeError as terr:
            file_path = path + re.sub(r"\W+", "", name) + '.' + suffix
        
        logger.info('Created file path: %s', file_path)
        return file_path
    
    @classmethod
    def formatParagraphsToString(cls, paragraphs):
        '''
        Formats text from several paragraphs to one string and replaces \<br\> tags with \\n.
        @param cls: This class to reference class variables.
        @param paragraphs: (list) The paragraphs that will be formatted to one text/string.  
        @return: (string) A newly formatted string that contains all the text from the paragraphs.
        '''
        rst_concatenated_string = ''
        if paragraphs:
            for paragraph in paragraphs:
                ''' The following method is not working. Don't know why. ''' 
        #        Lepistant.removeSubtreesFromSoup(paragraph, lambda: paragraph.br)
                
                ''' Removing the br tags here since the above method is not working. '''
                paragraph = cls.replaceBrTagsInSoup(paragraph, '\n')
                
                # Concatenating the content's lines by assigning them to rst_concatenated_string
                for line in paragraph.contents:
                    rst_concatenated_string += line.string
                    
            # Removing double blank lines.
            rst_concatenated_string = rst_concatenated_string.replace('\n\r', '\n')
            rst_concatenated_string = rst_concatenated_string.replace('\n\n', '\n')
            # Removing extra spaces.
    #        rst_concatenated_string = re.sub(r'  +', ' ', rst_concatenated_string)
                
        return rst_concatenated_string
    
    @classmethod
    def getSoup(cls, url, file_path):
        '''
        Gets soup from a webpage/file and pickles the soup if it was fetched from a webpage.
        @param cls: This class to reference class variables.
        @param url: URL of the webpage from which to fetch the soup.
        @param fileName: File name of pickled soup, if it was pickled before otherwise it is 
        used as the file name under which the fetched soup will be pickled.
        @return: (string) soup -A soup in form of a string, if succeeded and an empty string, 
        if no soup could be fetched
        '''
        rst_soup = ''
        webpage = ''
        
        try:
            # Check if there is a pickled rst_soup for file name.
            with open(file_path, 'rb') as from_file_name:
                webpage = pickle.load(from_file_name)
            logger.info('Retrieved webpage "%s" as a soup string from disk.', file_path)
        except IOError as err:
            logger.warning('Failed to open file "%s" due to: %s', url, str(err))
            logger.info('Start downloading webpage from the internet instead')
            try:
                # Get HTML code from the URL addresss.
                webpage = urllib2.urlopen(url)
            except urllib2.URLError as urlerr:
                logger.error('Failed to fetch webpage "%s" due to: %s', url, str(urlerr))
        except pickle.PickleError as perr:
            logger.warning('Failed to pickle webpage "%s" due to: %s', url, str(perr))
         
        try:
            # Cook a rst_soup from the fetched HTML code of the webpage.    
            rst_soup = BeautifulSoup(webpage)
            # Pickle rst_soup content for later usage.
            Lepistant.pickleSoup(rst_soup, file_path)
        except HTMLParser.HTMLParseError as htmlerr:
            logger.warning('Failed to parse rst_soup from "%s" due to: ', file_path, str(htmlerr))
            
        return rst_soup
    
    @classmethod
    def getTagsByClass(cls, soup, tag, css_class):
        '''
        Gets all tags that uses a specific CSS class.
        @param cls: This class to reference class variables.
        @param soup: The soup containin the HTML code that will be inspected.
        @param tag: The HTML tag that uses the specified CSS class.
        @param css_class: 
        '''
        rst_tag_list = []
        try:
            rst_tag_list = soup.findAll(tag, {"class": css_class})
        except TypeError as terr:
            logger.error('Failed parsing soup due to: %s - Returning an empty list instead.', str(terr))
        
        return rst_tag_list
        
    @classmethod
    def getURLFromImageTag(cls, img_tag):
        '''
        Gets the URL of the image (jpg, png or gif)
        @param cls: This class to reference class variables.
        @param img_tag: The image tag that contains the url in its src attribute.
        '''
        rst_url = cls.NOT_AVAILABLE
        
        try:
            src_attr = img_tag['src']
            rst_url = re.search('http:\/\/(?!.*?http:\/\/).*\.(jpg|png|gif)', src_attr).group(0)
        except:
            logger.warning('Could not find any src attribute in img_tag "%s". Setting url to "%s"', img_tag, cls.NOT_AVAILABLE)
        
        return rst_url 
    
    @classmethod
    def getURLFromTagContent(cls, tag_content):
        '''
        Gets the URL of a link ('<a>' tag) from an HTML tag.
        @param cls: This class to reference class variables.
        @param tag: Tag that contains the <a> tag with the URL address.
        @return: (string) rst_url - The URL address in form a string. 
        '''
        rst_url = ''
    
        try:
            rst_url = tag_content.a.attrs[0][1]
            if (not rst_url.startswith('http://')):
                rst_url = cls.URL_PREFIX + rst_url
        except:
            logger.warning('Could not find any url in tag_content "%s". Setting url to empty string', tag_content)
            
        return rst_url
    
    @classmethod
    def pickleSoup(cls, soup, file_path):
        '''
        Pickles a soup in form of string for later usage.
        @param cls: This class to reference class variables.
        @param soup: The soup to pickle.
        @param fileName: The file name under which the soup should be pickled.
        '''
        # Extracting the folder_path from the file_path
        # file_path: '../../../../downloads/plays/AltArmArbeitslos.html' > folder_paty: '../../../../downloads/plays/' 
        folder_path =  file_path.rsplit('/', 1)[0]
        # Create 'downloads' directory for saving files if the directory does not exist.
        if not os.path.isdir(folder_path):
            try:
                os.makedirs(folder_path)
            except OSError as oserr:
                logger.warning('Failed to create folder "%s" due to: %s', folder_path, str(oserr))
            else:
                return
        
        # Only pickle file if the file does not exist.
        file_exists = os.path.isfile(file_path)
        if not file_exists:
            try:
                with open(file_path, 'wb') as to_file_path:
                    pickle.dump(str(soup), to_file_path)
            except PickleError as perr:
                logger.warning('Failed to pickle soup due to: %s', str(perr))
    
    @classmethod
    def removeSubtreesFromSoup(cls, soup, f_subtree):
        '''
        @warning: This method is not working. The while condition skips one tag.
        Removes all subtrees from a soup.
        @param soup: The soup from which to remove the subtrees.
        @param subtree: A lambda expression that determines the subtree(s) (its a path to a tag) 
                        that will be removed.
        '''
        # while condition does not work correctly.
        while f_subtree():
            f_subtree = f_subtree()
            f_subtree.extract()
    
    @classmethod
    def replaceBrTagsInSoup(self, soup, tag_replacement):
        while soup.br:
            soup.br.replaceWith('\n')
            
        return soup
            
    @classmethod
    def setInfo(cls, info):
        cls.info = info
        cls.CSS_CLASS_CONTENT_ITEM = info[cls.KEY_CSS_CLASS_CONTENT_ITEM]
        cls.FILE_NAME_LEPORELLO = info[cls.KEY_THEATRE]
        cls.URL_PREFIX = info[cls.KEY_URL_PREFIX]
        
    
        
    
        
    