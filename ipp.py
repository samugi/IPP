import urllib
import subprocess
import json
import configparser
import datetime
from datetime import date

config = configparser.ConfigParser()
config.sections()
config.read('config.txt')

ACCESS_TOKEN = config['DEFAULT']['accessToken']
INSTAGRAM_BUSINESS_USER_ID = config['DEFAULT']['instagramBusinessUserId']
FACEBOOK_APP_ID= config['DEFAULT']['facebookAppId']
FACEBOOK_APP_SECRET= config['DEFAULT']['facebookAppSecret']


#Getting a refresh token if not yet refreshed today
lastRefresh = datetime.datetime.strptime(config['DEFAULT']['lastTokenRefresh'],"%Y-%m-%d")  if config['DEFAULT']['lastTokenRefresh'] != "" else datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')
print("last refr: " + str(lastRefresh))
if (datetime.datetime.now() - lastRefresh).days > 0 :
    print("Refreshing token...")
    getRefreshToken_curl_cmd = ['curl',
                  "https://graph.facebook.com/v5.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+FACEBOOK_APP_ID+"&client_secret="+FACEBOOK_APP_SECRET+"&fb_exchange_token="+ACCESS_TOKEN]
    getRefreshToken_response = subprocess.Popen(getRefreshToken_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0].decode("utf-8") 
    ACCESS_TOKEN = json.loads(getRefreshToken_response)["access_token"]
    #Update last token and refresh date in config file
    config['DEFAULT']['lastTokenRefresh'] = date.today().strftime("%Y-%m-%d")
    config['DEFAULT']['accessToken'] = ACCESS_TOKEN
    with open('config.txt', 'w') as configfile:
        config.write(configfile)


#Executing a request with our new token, fetching all media for INSTAGRAM_BUSINESS_USER_ID
oauth_curl_cmd = ['curl',
                  "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?access_token=" + ACCESS_TOKEN]
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

print ("Response: " + str(oauth_response))