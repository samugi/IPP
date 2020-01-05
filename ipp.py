import urllib
import json
import configparser
import datetime
import autoScript
import time
from Comment import Comment
import cloudinary
import cloudinary.uploader
import cloudinary.api
import utils
import sys

if len(sys.argv) == 1:
    print("Usage: $python ipp.py <config_file>")
    exit()

config = configparser.ConfigParser()
config.sections()
config.read(sys.argv[1])

ACCESS_TOKEN = config['DEFAULT']['accessToken']
INSTAGRAM_BUSINESS_USER_ID = config['DEFAULT']['instagramBusinessUserId']
FACEBOOK_APP_ID= config['DEFAULT']['facebookAppId']
FACEBOOK_APP_SECRET= config['DEFAULT']['facebookAppSecret']
CLOUDINARY_CLOUD_NAME = config['CLOUDINARY']['cloud_name']
CLOUDINARY_API_KEY = config['CLOUDINARY']['api_key']
CLOUDINARY_API_SECRET = config['CLOUDINARY']['api_secret']

def findCommentPosition (jsonArr, commentId):
    for i in range(len(jsonArr)):
        if jsonArr[i]["id"] == commentId:
           return i
    return -1

#Setting up Cloudinary config
cloudinary.config( 
  cloud_name = CLOUDINARY_CLOUD_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET 
)



#Getting a refresh token if not yet refreshed today
lastRefresh = datetime.datetime.strptime(config['DEFAULT']['lastTokenRefresh'],"%Y-%m-%d")  if config['DEFAULT']['lastTokenRefresh'] != "" else datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')

if (datetime.datetime.now() - lastRefresh).days > 0 :
    print("Refreshing token...") 
    getRefreshToken_response = utils.execWithOutput(['curl',
                  "https://graph.facebook.com/v5.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+FACEBOOK_APP_ID+"&client_secret="+FACEBOOK_APP_SECRET+"&fb_exchange_token="+ACCESS_TOKEN]) 
    ACCESS_TOKEN = json.loads(getRefreshToken_response)["access_token"]
    #Update last token and refresh date in config file
    config['DEFAULT']['lastTokenRefresh'] = datetime.datetime.now().strftime("%Y-%m-%d")
    config['DEFAULT']['accessToken'] = ACCESS_TOKEN
    with open('config.txt', 'w') as configfile:
        config.write(configfile)

lastPostCheck = datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')

while True:
    #If never checked in the last hour...
    if (datetime.datetime.now() - lastPostCheck).seconds//3600 > 0 :
        print("Taking a screenshot")
        utils.stampWindowPath("./screenshots/", str(round(time.time()))+".jpg")
        print("Fetcing last post foar IG business user. Wait 18 seconds...")
        lastPostCheck = datetime.datetime.now()
        #Fetching last post for INSTAGRAM_BUSINESS_USER_ID
        media_response =  utils.execWithOutput(['curl', "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?access_token=" + ACCESS_TOKEN])
        #Fetching last post from IG                                
        lastPost = json.loads(media_response)["data"][0]["id"]
        time.sleep(18)

    #Fetching all comments from last post
    print("Fetcing all comments from last post...")
    comments_response = utils.execWithOutput(['curl', "https://graph.facebook.com/v5.0/" + lastPost + "/comments?fields=like_count,hidden,id,media,text,timestamp,username,replies,user&access_token=" + ACCESS_TOKEN])
    commentsJArr = json.loads(comments_response)["data"]
    #Getting the position in the array "comments" of the last used comment 
    lastUsedCommentPosition = findCommentPosition(commentsJArr, config['DEFAULT']['lastUsedCommentId']) if config['DEFAULT']['lastUsedCommentId'] != "" else -1

    #Fetching the next comment from the array
    nextCommentIndex = lastUsedCommentPosition - 1 if lastUsedCommentPosition > 0 else lastUsedCommentPosition
    nextComment = commentsJArr[nextCommentIndex]
    nextCommentText = nextComment["text"]

    #Creating list of our Comment Objects
    commentsList = utils.fillCommentsList(nextCommentIndex, commentsJArr)

    #Updating the last used comment in the configs
    config['DEFAULT']['lastUsedCommentId'] = commentsJArr[0]["id"]
    with open('config.txt', 'w') as configfile:
            config.write(configfile)

    autoScript.controller(commentsList)
    print("Now sleeping for 20 sec")
    time.sleep(20)


##start testing post media
#cloudinary.uploader.upload("my_picture.jpg", public_id = 'abcdefg')
#url = cloudinary.utils.cloudinary_url("abcdefg.jpg")
##not available due to instagram limitations: only partners can post via API
#post_curl_cmd = ['curl', '-X',
#    'POST',
#                "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?image_url=" + url[0] + "?access_token=" + ACCESS_TOKEN + "&caption=#poketest"]
#print("siamo qui 2")                
#post_response = subprocess.Popen(post_curl_cmd,
#                                stdout = subprocess.PIPE,
#                                stderr = subprocess.PIPE).communicate()[0]
#print(post_response)
#exit()
##end testing post media