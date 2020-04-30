# coding=utf-8

VERSION_NUMBER = '1.3.0'

import os,feedparser,urllib.parse,parsehtml,twatter,re,time,tweepy,sys
from configparser import SafeConfigParser, ConfigParser
import importlib

importlib.reload(sys)

time.sleep(1)

print ('-------------------------------------')
print ('Reading config & data files')
configparser = ConfigParser()
configparser.read('config.cfg')

#Twitter credentials
TWITTER_CONSUMER_KEY = configparser.get('TWITTER_CREDENTIALS', 'consumer_key')
TWITTER_CONSUMER_SECRET = configparser.get('TWITTER_CREDENTIALS', 'consumer_secret')
TWITTER_ACCESS_TOKEN = configparser.get('TWITTER_CREDENTIALS', 'access_token')
TWITTER_ACCESS_TOKEN_SECRET = configparser.get('TWITTER_CREDENTIALS', 'access_token_secret')

#In 'data' file we store the latest post ID that we tweeted
data = open('data', 'r')
old_id = data.read()

#Lets tell them who we are, incase they are wondering who is accessing their RSS feed every minute
print ('Fetching RSS feed')
feedparser.USER_AGENT = "OVHStatusTwatBot/" + VERSION_NUMBER + " +https://twitter.com/ovh_status"
d = feedparser.parse('http://travaux.ovh.com/rss.php')

"""
17.7.2017: For some reason OVH status pages sometimes spits polish version, fucking up everything.
The following logic checks that the rss feed we got is the right one: OVH Travaux from the feed title
"""

print((d['feed']['title']))

if d['feed']['title'] != "OVH Travaux":
    print ("not OVH Travaux. Exiting!")
    exit(0)

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
    parsedurl = urllib.parse.urlparse(url)
    id = urllib.parse.parse_qs(parsedurl.query)['id'].pop()
    
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
    print ('No change in feed. Terminating program')
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
        tweeturl = orgurl
        title = d.entries[entry].title
        description = d.entries[entry].description
        description = parsehtml.strip(description)
        description.encode('utf-8')

        
        if "FS#" in title:
            #In this section we remove unnecessary FS#NUMBER thing from tweet
            #\xe2\x80\x94 = Long dash
            delimiters = "::", '\xe2\x80\x94 '
            regexPattern = '|'.join(map(re.escape, delimiters))
            parsedtitle = re.split(regexPattern, title.encode('utf-8'))
            title = parsedtitle[0] + " | " + parsedtitle[2]       

        if "Serveurs dédiés::" in title:
            parsedtitle = title.split("::")
            title = "Dedicated::" + parsedtitle[1]

        if "Noms de domaine::" in title:
            parsedtitle = title.split("::")
            title = "Domain::" + parsedtitle[1]

        if "Reseau Internet et Baies::" in title:
            parsedtitle = title.split("::")
            title = "Network::" + parsedtitle[1]

        if "Hébergements web::" in title:
            parsedtitle = title.split("::")
            title = "Web hosting::" + parsedtitle[1]



        
        #Joining title and parsed description together
        tweetText = title + ": " + description

        tweetText.encode('utf-8')
        #Lenght of tweeturl
        ltweeturl = len(tweeturl)
        tweetLenght = 280
	#280

        #For twitters t.co link bullshit and one for space, two for dots and #OVH
        tweetLenght -= 35

        #If tweet is too long, make it shorter
        if len(tweetText) > tweetLenght:
            tweetText = (tweetText[:tweetLenght] + '..')
        tweet = tweetText + ' ' + tweeturl + ' #ovh'
	#Checking that tweet IS less than allowed once more, and if not. it will cut it as much as it needs to be shortened.
        if len(tweetText) > tweetLenght:
           print((len(tweetText) - tweetLenght))
           newlength = len(tweetText) - tweetLenght
           newlength = tweetLenght - newlength
           tweetText = tweetText[:tweetLenght]
           print ("Lets see")
           print((len(tweetText)))    
		

        tweet = tweetText + ' ' + tweeturl + ' #ovh'
        print((len(tweet)))
        

        print ('Tweeting..')
        
        try:
            twatter.tweet(tweet, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        except tweepy.TweepError as e:
            error_msg = '#####ERROR#####\n' + time.strftime("%c") + '\n' + e.message[0]['message'] + '\nTweetText: ' + tweet + '\n###############\n\n'
            #push.send(PUSHOVER_APP_API_TOKEN, PUSHOVER_USER_TOKEN, error_msg, 'OVHStatus')
            errorwrite = open('error.log', 'w')
            errorwrite.write(error_msg)
            errorwrite.close()
            print ('Error occurred. Check error.log')
            pass
        
        
        print ('Tweet sent!')
        
            
    
"""
End of loop
"""

print ('Writing new ID to data file')

datawrite = open('data', 'w')
newvalue = max(highestvalue)
datawrite.write(newvalue)
datawrite.close()



print ('Everything that I can do has been done. Terminating..')
exit(0)
