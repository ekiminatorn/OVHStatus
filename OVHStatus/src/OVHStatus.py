"""
--TODO--
1. Add a check that checks for t.co address lenght once per day
2. Support Pushbullet?
3. Support Pushover?
"""

VERSION_NUMBER = '1.1.0'

"""
SEMANTIC VERSIONING:
1. MAJOR version when you make incompatible API changes,
2. MINOR version when you add functionality in a backwards-compatible manner, and
3. PATCH version when you make backwards-compatible bug fixes.
"""

import os,feedparser,urlparse,shortenurl,parsehtml,twatter,test,re
from ConfigParser import SafeConfigParser, ConfigParser


print 'Reading config & data files'
configparser = SafeConfigParser()
configparser.read('config.cfg')
#URL Shortener service API key
URL_SHORT_API_KEY = configparser.get('URL_SHORTENER_SERVICE', 'api_key')
URL_SHORT_IP = configparser.get('URL_SHORTENER_SERVICE', 'ip')

#Twitter credentials
TWITTER_CONSUMER_KEY = configparser.get('TWITTER_CREDENTIALS', 'consumer_key')
TWITTER_CONSUMER_SECRET = configparser.get('TWITTER_CREDENTIALS', 'consumer_secret')
TWITTER_ACCESS_TOKEN = configparser.get('TWITTER_CREDENTIALS', 'access_token')
TWITTER_ACCESS_TOKEN_SECRET = configparser.get('TWITTER_CREDENTIALS', 'access_token_secret')

#In 'data' file we store the latest post ID that we tweeted
data = open('data', 'r')
old_id = data.read()


#Lets tell them who we are, incase they are wondering who is accessing their RSS feed every minute
print 'Fetching RSS feed'
feedparser.USER_AGENT = "OVHStatusTwatBot/" + VERSION_NUMBER + " +https://twitter.com/ovh_status"
d = feedparser.parse('http://status.ovh.com/rss.php')


"""
In this for loop, we go through all entries, parsing their guid (url) to get the unique ID of entry.
phonebook: Dictionary for all the IDs.
n1: number1
"""

highestvalue = []
phonebook = {}
n1 = 0

for post in d.entries:
    
    url = post.guid
    parsedurl = urlparse.urlparse(url)
    id = urlparse.parse_qs(parsedurl.query)['id'].pop()
    
    """
    Highestvalue array is my lazy way of using max() down the line to get the newest post ID, so I can update data file
    """
    highestvalue.append(id)
    
 
    phonebook[id] = n1
    n1 += 1    
"""
End of loop
"""

#Check if feed has been updated, if not, exit.
if old_id == max(highestvalue):
    print 'No change in feed. Terminating program'
    exit(0)
    


"""
This is the loop where all the magic happens.
Comparing the latest ID that we have tweeted to all entries in the feed, and tweeting out those which values are greater.
Also doing some parsing, and decreasing the info into acceptable tweet (140 chars)
"""

for post in phonebook:
    if post > old_id:
       
        entry = phonebook.get(post)
        orgurl = d.entries[entry].link
        
        #Shorten URL
        tweeturl = shortenurl.short(orgurl, URL_SHORT_API_KEY, URL_SHORT_IP, VERSION_NUMBER)
        title = d.entries[entry].title
        description = d.entries[entry].description
        description = parsehtml.strip(description)
        
        
        #In this section we remove unnecessary FS#NUMBER thing from tweet
        #\xe2\x80\x94 = Long dash
        delimiters = "::", '\xe2\x80\x94 '
        regexPattern = '|'.join(map(re.escape, delimiters))
        parsedtitle = re.split(regexPattern, title.encode('utf-8'))
        title = parsedtitle[0] + " | " + parsedtitle[2]       
        
        #Joining title and parsed description together
        tweetText = title + ": " + description
        
        #Lenght of tweeturl
        ltweeturl = len(tweeturl)
        tweetLenght = 140

        #For twitters t.co link bullshit and one for space, two for dots
        tweetLenght -= 25


        #If tweet is too long, make it shorter
        if len(tweetText) > tweetLenght:
            tweetText = (tweetText[:tweetLenght] + '..')
            
        tweet = tweetText + ' ' + tweeturl

        

        print 'Tweeting..'
        
        twatter.tweet(tweet, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        
        print 'Tweet sent!'
        
            
    
"""
End of loop
"""

print 'Writing new ID to data file'

datawrite = open('data', 'w')
newvalue = max(highestvalue)
datawrite.write(newvalue)
datawrite.close()



print 'Everything that I can do has been done. Terminating..'
exit(0)
        

















