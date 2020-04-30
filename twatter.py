import tweepy

def tweet(tweet, consumer_key, consumer_secret, access_token, access_token_secret):
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth)
    
    print 'If auth was successful, we should see username now:'
    print(api.me().name)
    
    api.update_status(status=tweet)

