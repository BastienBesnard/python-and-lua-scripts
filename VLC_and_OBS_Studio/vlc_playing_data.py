import os, time, datetime, requests, codecs
import xml.etree.ElementTree as ET

try:
    # Python 2.6-2.7 
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

# CONFIG
PASSWORD = 'password'
TITLE_PLAYING_FILE_NAME = 'TITLE_PLAYING.txt'
TIME_START_PLAYING_FILE_NAME = 'TIME_START_PLAYING.txt'
SLEEP_NB_SECONDS = 5

# Global variable to keep track of the info being printed and check for changes
CURRENT_INFO = ''

def getInfo():
    global PASSWORD

    # CUSTOM: Separator can be changed to whatever you want
    separator = '   |   '

    title = 'UNKNOWN'
    artist = 'UNKNOWN'
    fileName = ''
    time = 0
    
    s = requests.Session()
    
    # Username is blank
    s.auth = ('', PASSWORD)
    
    # Attempt to retrieve info from the web interface
    try:
        r = s.get('http://localhost:8080/requests/status.xml', verify=False)
        
        if('401 Client error' in r.text):
            print('Web Interface Error: Do the passwords match as described in the README.txt?')
            return
    except:
        print('Web Interface Error: Is VLC running? Did you enable the Web Interface as described in the README.txt?')
        return

    # Save the response data
    root = ET.fromstring(r.content)

    # Get the time to compute start playing time
    timeNode = root.find('time')
    if timeNode is not None:
        try:
            time = int(timeNode.text)
        except ValueError:
            time = 0
    
    # Loop through all info nodes to find relevant metadata
    for info in root.iter('info'):
        # Save the name attribute of the info node
        name = info.get('name')
         
        # See if the info node we are looking at is for the title
        if(name == 'title'):
            title = info.text

    if( title != 'UNKNOWN' ):
        writeInfoToFile(title, time, separator)
    else:
        writeInfoToFile('', time, '')
# END: getInfo()

def writeInfoToFile( info, time, separator ):
    global TITLE_PLAYING_FILE_NAME
    global CURRENT_INFO
    htmlParser = HTMLParser()
    
    if(CURRENT_INFO != info):
        CURRENT_INFO = info

        # Title playing
        print('Title: ' + htmlParser.unescape(CURRENT_INFO))
        textFile = codecs.open(TITLE_PLAYING_FILE_NAME, 'w', encoding='utf-8', errors='ignore')
        textFile.write(htmlParser.unescape(CURRENT_INFO + separator))
        textFile.close()

        # Time start playing
        computedTime = datetime.datetime.now() + datetime.timedelta(seconds=-time)
        textFile = codecs.open(TIME_START_PLAYING_FILE_NAME, 'w', encoding='utf-8', errors='ignore')
        print('Start time: ' + computedTime.strftime('%d/%m/%Y %H:%M:%S'))
        textFile.write(computedTime.strftime('%Y;%m;%d;%H;%M;%S'))
        textFile.close()
# END: writeInfoToFile( info, time, separator )

if __name__ == '__main__':
    while 1:
        getInfo()
        
        # Sleep for a number of seconds before checking again
        time.sleep(SLEEP_NB_SECONDS)
# END: if __name__ == '__main__'
