import requests,json,urllib

"""
Shortening URL to own custom URL function
"""
def short(url, api, ip, version):

    #Parameters for the URL
    payload = {'signature': api, 'action': 'shorturl', 'url': url, 'format': 'json'}
    
    user_agent = {'User-agent': 'OVHStatusTwatBot/' + version + ' +http://twitter.com/ovh_status'}
    response = requests.get(ip, params=payload, headers = user_agent)  
    
    #Getting short url from JSON response
    data = json.loads(response.text)
    
    #Returning data
    return data['shorturl']

    